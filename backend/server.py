from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import logging
from pathlib import Path
from datetime import datetime
import uuid
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from bson import ObjectId
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
import json

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
mongo_url = os.environ['MONGO_URL']
database_name = os.environ['DB_NAME']
client = None
db = None

# Global payment clients
stripe_checkout = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global client, db, stripe_checkout
    
    # Initialize MongoDB
    client = AsyncIOMotorClient(mongo_url)
    db = client[database_name]
    
    # Initialize Stripe
    stripe_api_key = os.environ.get('STRIPE_API_KEY')
    if stripe_api_key:
        # Use a placeholder webhook URL for now
        webhook_url = "http://localhost:8001/api/webhook/stripe"
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
        logger.info("Stripe checkout initialized")
    
    logger.info("Database and payment services initialized")
    
    yield
    
    # Shutdown
    if client:
        client.close()
    logger.info("Application shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title="DE---NINE Art Store API",
    description="Premium art print e-commerce API with multi-payment support",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Configure this properly in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API router
api_router = APIRouter(prefix="/api")

# Pydantic models
from pydantic import ConfigDict
from pydantic_core import core_schema
from typing_extensions import Annotated

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)
    
    @classmethod
    def validate(cls, value, info=None):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId')
        return ObjectId(value)

    def __str__(self):
        return str(self)

class PrintVariant(BaseModel):
    id: str
    name: str
    image_url: str
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PrintTheme(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    theme_id: str
    theme: str
    description: str
    base_price: int  # Price in øre/cents
    variants: List[PrintVariant]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CartItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    session_id: str
    user_id: Optional[str] = None
    theme_id: str
    selected_variants: List[str]
    quantity: int
    unit_price: int
    total_price: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentTransaction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    session_id: str
    payment_method: str  # "stripe", "paypal", "vipps"
    payment_id: str  # External payment ID
    amount: int  # Amount in øre/cents
    currency: str = "NOK"
    status: str = "pending"  # "pending", "completed", "failed", "refunded"
    payment_status: str = "initiated"
    items: List[Dict[str, Any]] = []
    metadata: Dict[str, str] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Order(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    order_number: str
    session_id: str
    user_id: Optional[str] = None
    items: List[Dict[str, Any]]
    subtotal: int
    shipping_cost: int = 0  # Free shipping
    total: int
    status: str = "pending"  # "pending", "processing", "shipped", "delivered", "cancelled"
    payment_transaction_id: Optional[str] = None
    shipping_address: Optional[Dict[str, str]] = None
    customer_info: Optional[Dict[str, str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response models
class CreatePaymentRequest(BaseModel):
    items: List[Dict[str, Any]]
    customer_info: Dict[str, str]
    payment_method: str = "stripe"
    
class CheckoutRequest(BaseModel):
    session_id: str
    customer_info: Dict[str, str]
    payment_method: str = "stripe"

# Database dependency
async def get_database():
    return db

# Helper functions
def generate_order_number() -> str:
    """Generate unique order number"""
    return f"DN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

async def calculate_cart_total(session_id: str) -> Dict[str, Any]:
    """Calculate cart totals"""
    cart_items = await db.cart_items.find({"session_id": session_id}).to_list(1000)
    
    # Convert ObjectId to string for JSON serialization
    for item in cart_items:
        item["id"] = str(item["_id"])
        del item["_id"]
    
    subtotal = sum(item["total_price"] for item in cart_items)
    shipping = 0  # Free shipping
    total = subtotal + shipping
    
    return {
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "items": cart_items
    }

# API Endpoints

# Print Management
@api_router.get("/prints")
async def get_all_prints(db=Depends(get_database)):
    """Get all print themes with their variants"""
    try:
        prints_cursor = db.print_themes.find({})
        prints = await prints_cursor.to_list(1000)
        
        # Convert ObjectId to string for JSON serialization
        for print_item in prints:
            print_item["id"] = str(print_item["_id"])
            del print_item["_id"]
            
        return {"prints": prints}
    except Exception as e:
        logger.error(f"Error fetching prints: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch prints")

@api_router.get("/prints/{theme_id}")
async def get_print_theme(theme_id: str, db=Depends(get_database)):
    """Get specific print theme with all variants"""
    try:
        print_theme = await db.print_themes.find_one({"theme_id": theme_id})
        if not print_theme:
            raise HTTPException(status_code=404, detail="Print theme not found")
            
        print_theme["id"] = str(print_theme["_id"])
        del print_theme["_id"]
        
        return print_theme
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching print theme {theme_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch print theme")

# Cart Management
@api_router.get("/cart/{session_id}")
async def get_cart(session_id: str, db=Depends(get_database)):
    """Get cart contents for session"""
    try:
        cart_data = await calculate_cart_total(session_id)
        return cart_data
    except Exception as e:
        logger.error(f"Error fetching cart for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch cart")

@api_router.post("/cart/{session_id}/add")
async def add_to_cart(
    session_id: str, 
    item_data: Dict[str, Any], 
    db=Depends(get_database)
):
    """Add item to cart"""
    try:
        # Create cart item
        cart_item = CartItem(
            session_id=session_id,
            theme_id=item_data["theme_id"],
            selected_variants=item_data["selected_variants"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"],
            total_price=item_data["unit_price"] * item_data["quantity"]
        )
        
        # Insert into database
        await db.cart_items.insert_one(cart_item.dict(by_alias=True, exclude_unset=True))
        
        # Return updated cart
        cart_data = await calculate_cart_total(session_id)
        return cart_data
    except Exception as e:
        logger.error(f"Error adding item to cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add item to cart")

@api_router.delete("/cart/{session_id}/item/{item_id}")
async def remove_from_cart(
    session_id: str, 
    item_id: str, 
    db=Depends(get_database)
):
    """Remove item from cart"""
    try:
        # Remove item
        result = await db.cart_items.delete_one({
            "_id": ObjectId(item_id),
            "session_id": session_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        # Return updated cart
        cart_data = await calculate_cart_total(session_id)
        return cart_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing item from cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to remove item from cart")

@api_router.delete("/cart/{session_id}")
async def clear_cart(session_id: str, db=Depends(get_database)):
    """Clear entire cart"""
    try:
        await db.cart_items.delete_many({"session_id": session_id})
        return {"message": "Cart cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear cart")

# Payment endpoints
@api_router.post("/payments/checkout")
async def create_checkout_session(
    request: Request,
    checkout_data: CheckoutRequest,
    db=Depends(get_database)
):
    """Create payment checkout session"""
    try:
        # Get cart data
        cart_data = await calculate_cart_total(checkout_data.session_id)
        
        if not cart_data["items"]:
            raise HTTPException(status_code=400, detail="Cart is empty")
        
        # Get host URL from request
        host_url = str(request.base_url).rstrip('/')
        
        # Prepare checkout session
        amount = float(cart_data["total"]) / 100  # Convert øre to kroner
        success_url = f"{host_url.replace('8001', '3000')}/payment/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{host_url.replace('8001', '3000')}/payment/cancel"
        
        checkout_request = CheckoutSessionRequest(
            amount=amount,
            currency="NOK",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "session_id": checkout_data.session_id,
                "payment_method": checkout_data.payment_method,
                "customer_email": checkout_data.customer_info.get("email", ""),
                "item_count": str(len(cart_data["items"]))
            }
        )
        
        # Create Stripe checkout session
        if checkout_data.payment_method == "stripe":
            session = await stripe_checkout.create_checkout_session(checkout_request)
            
            # Create payment transaction record
            payment_transaction = PaymentTransaction(
                session_id=checkout_data.session_id,
                payment_method="stripe",
                payment_id=session.session_id,
                amount=cart_data["total"],
                currency="NOK",
                status="pending",
                payment_status="initiated",
                items=cart_data["items"],
                metadata=checkout_request.metadata or {}
            )
            
            await db.payment_transactions.insert_one(
                payment_transaction.dict(by_alias=True, exclude_unset=True)
            )
            
            return {
                "checkout_url": session.url,
                "session_id": session.session_id,
                "amount": amount,
                "currency": "NOK"
            }
        
        else:
            raise HTTPException(status_code=400, detail="Payment method not supported yet")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating checkout session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create checkout session")

@api_router.get("/payments/status/{session_id}")
async def get_payment_status(
    session_id: str,
    db=Depends(get_database)
):
    """Get payment status"""
    try:
        # Check payment status with Stripe
        checkout_status = await stripe_checkout.get_checkout_status(session_id)
        
        # Update payment transaction in database
        await db.payment_transactions.update_one(
            {"payment_id": session_id},
            {"$set": {
                "status": "completed" if checkout_status.payment_status == "paid" else checkout_status.status,
                "payment_status": checkout_status.payment_status,
                "updated_at": datetime.utcnow()
            }}
        )
        
        # If payment is successful, create order
        if checkout_status.payment_status == "paid":
            await process_successful_payment(session_id, db)
        
        return {
            "session_id": session_id,
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "amount_total": checkout_status.amount_total,
            "currency": checkout_status.currency
        }
        
    except Exception as e:
        logger.error(f"Error getting payment status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get payment status")

async def process_successful_payment(payment_session_id: str, db):
    """Process successful payment and create order"""
    try:
        # Get payment transaction
        payment = await db.payment_transactions.find_one({"payment_id": payment_session_id})
        if not payment:
            logger.error(f"Payment transaction not found: {payment_session_id}")
            return
        
        # Check if order already exists
        existing_order = await db.orders.find_one({"payment_transaction_id": payment_session_id})
        if existing_order:
            logger.info(f"Order already exists for payment: {payment_session_id}")
            return
        
        # Create order
        order = Order(
            order_number=generate_order_number(),
            session_id=payment["session_id"],
            items=payment["items"],
            subtotal=payment["amount"],
            total=payment["amount"],
            status="processing",
            payment_transaction_id=payment_session_id,
            customer_info=payment.get("metadata", {})
        )
        
        await db.orders.insert_one(order.dict(by_alias=True, exclude_unset=True))
        
        # Clear cart
        await db.cart_items.delete_many({"session_id": payment["session_id"]})
        
        logger.info(f"Order created successfully: {order.order_number}")
        
    except Exception as e:
        logger.error(f"Error processing successful payment: {str(e)}")

# Stripe webhook endpoint
@api_router.post("/webhook/stripe")
async def stripe_webhook(
    request: Request,
    db=Depends(get_database)
):
    """Handle Stripe webhook notifications"""
    try:
        body = await request.body()
        stripe_signature = request.headers.get("Stripe-Signature", "")
        
        # Handle webhook with stripe checkout
        webhook_response = await stripe_checkout.handle_webhook(body, stripe_signature)
        
        # Process webhook event
        if webhook_response.event_type == "checkout.session.completed":
            await process_successful_payment(webhook_response.session_id, db)
        
        return {"received": True}
        
    except Exception as e:
        logger.error(f"Error processing Stripe webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

# Orders endpoint
@api_router.get("/orders/{session_id}")
async def get_orders(
    session_id: str,
    db=Depends(get_database)
):
    """Get orders for session"""
    try:
        orders_cursor = db.orders.find({"session_id": session_id}).sort("created_at", -1)
        orders = await orders_cursor.to_list(1000)
        
        # Convert ObjectId to string
        for order in orders:
            order["id"] = str(order["_id"])
            del order["_id"]
            
        return {"orders": orders}
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")

# Admin endpoints
@api_router.get("/admin/prints")
async def admin_get_prints(db=Depends(get_database)):
    """Admin: Get all prints with full details"""
    try:
        prints_cursor = db.print_themes.find({})
        prints = await prints_cursor.to_list(1000)
        
        # Convert ObjectId to string for JSON serialization
        for print_item in prints:
            print_item["id"] = str(print_item["_id"])
            del print_item["_id"]
            
        return {"prints": prints}
    except Exception as e:
        logger.error(f"Error fetching prints for admin: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch prints")

@api_router.put("/admin/prints/{theme_id}")
async def admin_update_print(
    theme_id: str,
    update_data: Dict[str, Any],
    db=Depends(get_database)
):
    """Admin: Update print theme"""
    try:
        # Update the print theme
        result = await db.print_themes.update_one(
            {"theme_id": theme_id},
            {
                "$set": {
                    **update_data,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Print theme not found")
        
        # Return updated print
        updated_print = await db.print_themes.find_one({"theme_id": theme_id})
        updated_print["id"] = str(updated_print["_id"])
        del updated_print["_id"]
        
        return updated_print
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating print {theme_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update print")

@api_router.post(\"/admin/prints\")
async def admin_create_print(
    print_data: Dict[str, Any],
    db=Depends(get_database)
):
    \"\"\"Admin: Create new print theme\"\"\"
    try:
        # Create new print theme with default variants
        new_print = {
            \"theme_id\": print_data[\"theme_id\"],
            \"theme\": print_data[\"theme\"],
            \"description\": print_data.get(\"description\", \"\"),
            \"base_price\": print_data.get(\"base_price\", 19900),
            \"variants\": [
                {
                    \"id\": f\"{print_data['theme_id']}-v1\",
                    \"name\": f\"{print_data['theme']} I\",
                    \"image_url\": \"https://via.placeholder.com/500x700?text=Upload+Image\",
                    \"featured\": True,
                    \"created_at\": datetime.utcnow()
                },
                {
                    \"id\": f\"{print_data['theme_id']}-v2\",
                    \"name\": f\"{print_data['theme']} II\",
                    \"image_url\": \"https://via.placeholder.com/500x700?text=Upload+Image\",
                    \"featured\": False,
                    \"created_at\": datetime.utcnow()
                },
                {
                    \"id\": f\"{print_data['theme_id']}-v3\",
                    \"name\": f\"{print_data['theme']} III\",
                    \"image_url\": \"https://via.placeholder.com/500x700?text=Upload+Image\",
                    \"featured\": False,
                    \"created_at\": datetime.utcnow()
                }
            ],
            \"created_at\": datetime.utcnow(),
            \"updated_at\": datetime.utcnow()
        }
        
        # Insert into database
        result = await db.print_themes.insert_one(new_print)
        
        # Return created print
        created_print = await db.print_themes.find_one({\"_id\": result.inserted_id})
        created_print[\"id\"] = str(created_print[\"_id\"])
        del created_print[\"_id\"]
        
        return created_print
    except Exception as e:
        logger.error(f\"Error creating print: {str(e)}\")
        raise HTTPException(status_code=500, detail=\"Failed to create print\")

@api_router.delete(\"/admin/prints/{theme_id}\")
async def admin_delete_print(
    theme_id: str,
    db=Depends(get_database)
):
    \"\"\"Admin: Delete print theme\"\"\"
    try:
        result = await db.print_themes.delete_one({\"theme_id\": theme_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=\"Print theme not found\")
        
        return {\"message\": \"Print theme deleted successfully\"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f\"Error deleting print {theme_id}: {str(e)}\")
        raise HTTPException(status_code=500, detail=\"Failed to delete print\")\n\n# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "DE---NINE Art Store API", "status": "running"}

# Health check
@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "denine-art-store",
        "timestamp": datetime.utcnow().isoformat()
    }

# Include the router
app.include_router(api_router)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)