const mongoose = require('mongoose');

const connectDB = async () => {
    try {
        // Using environment variables for configuration
        const dbURI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/internship';
        
        // Adding options to the connection
        const options = {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        };

        // Attempting to connect
        await mongoose.connect(dbURI, options);

        console.log('✅ MongoDB connected successfully');
    } catch (error) {
        console.error('❌ MongoDB connection error:', error.message);

        // Optional: Exit the process if the connection fails
        process.exit(1);
    }
};

module.exports = connectDB;
