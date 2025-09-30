#!/usr/bin/env python3
"""
Database initialization script for DE---NINE Art Store
This script populates the MongoDB database with the initial print themes and variants.
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

# Database configuration
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "denine_artstore"

# Print themes data (matching frontend mock data)
print_themes_data = [
    {
        "theme_id": "terra-flow-01",
        "theme": "Terra Flow",
        "description": "Abstract landscapes where earth meets water in flowing, organic forms. Each piece captures the natural dance between geological structures and flowing elements.",
        "base_price": 19900,  # 199 NOK in øre
        "variants": [
            {
                "id": "terra-flow-01-v1",
                "name": "Terra Flow I",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/rm1z8whc_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_9bf35ed4-f078-46f2-9c25-c575dcb1cb35.png",
                "featured": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "terra-flow-01-v2",
                "name": "Terra Flow II",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/t62y1oeq_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_3605bc9b-0df7-4471-abde-b6396993080f.png",
                "featured": False,
                "created_at": datetime.utcnow()
            },
            {
                "id": "terra-flow-01-v3",
                "name": "Terra Flow III",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/tcqy627x_igorrnilsen_httpss.mj.runaQN_mLP4b5g_httpss.mj.runLhZO5OcPAXo_-_972d700e-645e-4833-a51a-b9c3a2c4989f.png",
                "featured": False,
                "created_at": datetime.utcnow()
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "theme_id": "desert-convergence-02",
        "theme": "Desert Convergence",
        "description": "Where sand dunes meet rivers, creating mesmerizing patterns of contrast and harmony. The interplay of warm earth tones with cool water elements.",
        "base_price": 19900,
        "variants": [
            {
                "id": "desert-convergence-02-v1",
                "name": "Desert Convergence I",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/dsp4zzim_igorrnilsen_httpss.mj.runaQN_mLP4b5g_httpss.mj.runLhZO5OcPAXo_-_bde9ef52-47af-4c98-a035-8e3f9aa86523%20%281%29.png",
                "featured": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "desert-convergence-02-v2",
                "name": "Desert Convergence II",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/rm1z8whc_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_9bf35ed4-f078-46f2-9c25-c575dcb1cb35.png",
                "featured": False,
                "created_at": datetime.utcnow()
            },
            {
                "id": "desert-convergence-02-v3",
                "name": "Desert Convergence III",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/t62y1oeq_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_3605bc9b-0df7-4471-abde-b6396993080f.png",
                "featured": False,
                "created_at": datetime.utcnow()
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "theme_id": "arctic-formations-03",
        "theme": "Arctic Formations",
        "description": "Frozen landscapes captured from above, revealing the subtle beauty of ice patterns and geological formations in pristine wilderness.",
        "base_price": 19900,
        "variants": [
            {
                "id": "arctic-formations-03-v1",
                "name": "Arctic Formations I",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/tcqy627x_igorrnilsen_httpss.mj.runaQN_mLP4b5g_httpss.mj.runLhZO5OcPAXo_-_972d700e-645e-4833-a51a-b9c3a2c4989f.png",
                "featured": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "arctic-formations-03-v2",
                "name": "Arctic Formations II",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/dsp4zzim_igorrnilsen_httpss.mj.runaQN_mLP4b5g_httpss.mj.runLhZO5OcPAXo_-_bde9ef52-47af-4c98-a035-8e3f9aa86523%20%281%29.png",
                "featured": False,
                "created_at": datetime.utcnow()
            },
            {
                "id": "arctic-formations-03-v3",
                "name": "Arctic Formations III",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/rm1z8whc_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_9bf35ed4-f078-46f2-9c25-c575dcb1cb35.png",
                "featured": False,
                "created_at": datetime.utcnow()
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "theme_id": "elemental-rhythms-04",
        "theme": "Elemental Rhythms",
        "description": "Natural patterns emerge from the intersection of different landscapes, creating rhythmic compositions that speak to the earth's fundamental forces.",
        "base_price": 19900,
        "variants": [
            {
                "id": "elemental-rhythms-04-v1",
                "name": "Elemental Rhythms I",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/t62y1oeq_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_3605bc9b-0df7-4471-abde-b6396993080f.png",
                "featured": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "elemental-rhythms-04-v2",
                "name": "Elemental Rhythms II",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/tcqy627x_igorrnilsen_httpss.mj.runaQN_mLP4b5g_httpss.mj.runLhZO5OcPAXo_-_972d700e-645e-4833-a51a-b9c3a2c4989f.png",
                "featured": False,
                "created_at": datetime.utcnow()
            },
            {
                "id": "elemental-rhythms-04-v3",
                "name": "Elemental Rhythms III",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/dsp4zzim_igorrnilsen_httpss.mj.runaQN_mLP4b5g_httpss.mj.runLhZO5OcPAXo_-_bde9ef52-47af-4c98-a035-8e3f9aa86523%20%281%29.png",
                "featured": False,
                "created_at": datetime.utcnow()
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "theme_id": "mineral-veins-05",
        "theme": "Mineral Veins",
        "description": "Geological masterpieces revealed through aerial perspective, showcasing the earth's natural artistry in mineral deposits and erosion patterns.",
        "base_price": 19900,
        "variants": [
            {
                "id": "mineral-veins-05-v1",
                "name": "Mineral Veins I",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/dsp4zzim_igorrnilsen_httpss.mj.runaQN_mLP4b5g_httpss.mj.runLhZO5OcPAXo_-_bde9ef52-47af-4c98-a035-8e3f9aa86523%20%281%29.png",
                "featured": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "mineral-veins-05-v2",
                "name": "Mineral Veins II",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/rm1z8whc_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_9bf35ed4-f078-46f2-9c25-c575dcb1cb35.png",
                "featured": False,
                "created_at": datetime.utcnow()
            },
            {
                "id": "mineral-veins-05-v3",
                "name": "Mineral Veins III",
                "image_url": "https://customer-assets.emergentagent.com/job_d67d05e5-b65e-421b-93bc-daeca4d987b4/artifacts/t62y1oeq_igorrnilsen_httpss.mj.runLhZO5OcPAXo_httpss.mj.runfPq83MaA-g8_h_3605bc9b-0df7-4471-abde-b6396993080f.png",
                "featured": False,
                "created_at": datetime.utcnow()
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

async def init_database():
    """Initialize the database with print themes data"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        print(f"Connected to MongoDB: {DB_NAME}")
        
        # Clear existing data
        await db.print_themes.delete_many({})
        print("Cleared existing print themes")
        
        # Insert print themes
        result = await db.print_themes.insert_many(print_themes_data)
        print(f"Inserted {len(result.inserted_ids)} print themes")
        
        # Create indexes for better performance
        await db.print_themes.create_index("theme_id", unique=True)
        await db.cart_items.create_index("session_id")
        await db.payment_transactions.create_index("payment_id", unique=True)
        await db.payment_transactions.create_index("session_id")
        await db.orders.create_index("order_number", unique=True)
        await db.orders.create_index("session_id")
        
        print("Database indexes created")
        
        # Verify data
        count = await db.print_themes.count_documents({})
        print(f"Verification: {count} print themes in database")
        
        # Close connection
        client.close()
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    print("Initializing DE---NINE Art Store database...")
    asyncio.run(init_database())