// utils/db.js
import mongoose from 'mongoose';

let isConnected = false; // Track if connection is already established

export async function connectDB() {
  if (isConnected) {
    // Already connected
    return;
  }
  try {
    // Use your MongoDB URI
    await mongoose.connect(process.env.MONGODB_URI, {
      dbName: 'JobPortal', // example DB name
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    isConnected = true;
    console.log('MongoDB connected');
  } catch (error) {
    console.error('MongoDB connection error:', error);
  }
}
