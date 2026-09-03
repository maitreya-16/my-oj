const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  username: {
    type: DataTypes.STRING(255),
    allowNull: true,
  },
  teamname:{
    type: DataTypes.STRING(255),
    defaultValue:"TEAM",
    allowNull:false
  },
  password: {
    type: DataTypes.STRING(255),
    allowNull: true,
  },
  rc: {
    type: DataTypes.STRING(255),
    allowNull: true,
  },
  isjunior: {
    type: DataTypes.BOOLEAN,
    allowNull: false,
    defaultValue: false,
  },
  role:{
    type : DataTypes.STRING(100),
    allowNull:false,
    defaultValue:"USER"
  }
}, {
  tableName: 'user', // 👈 lowercase to avoid quoted "User"
  timestamps: false,
});

module.exports = User;
