const { Sequelize } = require('sequelize');
const dotenv = require('dotenv').config();
const fs = require('fs');
const path = require('path');

const sequelize = new Sequelize(process.env.DB_URL, {

  dialect: 'postgres',


  dialectOptions: {
    ssl: {
      require: true,
      rejectUnauthorized: true,
      ca: fs.readFileSync(path.join(__dirname, '..', 'certs', 'global-bundle.pem')),
    },
  },


  protocol: 'postgres',
  logging: false,
  define: {
    timestamps: true,
    underscored: true,
  },
});

// Test connection function
const testDBConnection = async () => {
  try {
    await sequelize.authenticate();
    return true;
  } catch (error) {
    console.error('❌ Unable to connect to the database:', error);
    return false;
  }
};

// Export the sequelize instance as default export
module.exports = sequelize;

// Export test function separately if needed
module.exports.testDBConnection = testDBConnection;
