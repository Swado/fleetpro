// Import required packages
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

// Create a new Prisma client instance
const prisma = new PrismaClient({
  // Add debug information - optional
  log: ['query', 'info', 'warn', 'error'],
});

async function main() {
  try {
    // Check if admin user exists
    console.log('Checking if admin user exists...');
    const existingUser = await prisma.$queryRaw`
      SELECT * FROM "User" WHERE username = 'admin' LIMIT 1;
    `;

    // If admin user doesn't exist, create one
    if (!existingUser || existingUser.length === 0) {
      console.log('Admin user does not exist. Creating...');
      
      // Hash the password
      const hashedPassword = await bcrypt.hash('admin123', 10);
      
      // Insert the admin user with a raw SQL query
      await prisma.$executeRaw`
        INSERT INTO "User" (username, email, password_hash, created_at, updated_at)
        VALUES ('admin', 'admin@example.com', ${hashedPassword}, now(), now());
      `;
      
      console.log('Admin user created successfully!');
    } else {
      console.log('Admin user already exists.');
    }
  } catch (error) {
    console.error('Error creating admin user:', error);
  } finally {
    // Close the Prisma client connection
    await prisma.$disconnect();
  }
}

// Run the main function
main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });