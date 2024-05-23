const { MongoClient } = require('mongodb');

async function setupDatabase() {
    const uri = "mongodb://localhost:27017"; // Replace with your MongoDB server URI
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    try {
        await client.connect();
        console.log("Connected successfully to server");

        const db = client.db("silk");

        // Create collections
        const collections = [
            "common_model"
        ];

        for (let collection of collections) {
            await db.createCollection(collection);
            console.log(`Collection '${collection}' created`);
        }

        // Create indexes for the hosts collection to optimize queries
        await db.collection('common_model').createIndex({ ip_address: 1 }, { unique: true });
        await db.collection('common_model').createIndex({ hostname: 1 });
        await db.collection('common_model').createIndex({ provider: 1 });

        console.log("Indexes created successfully");

    } catch (err) {
        console.error(err);
    } finally {
        await client.close();
    }
}

setupDatabase().catch(console.dir);
