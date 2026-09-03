// models/Leaderboard.js
const { DataTypes } = require("sequelize");
const sequelize = require("../config/database");

const Leaderboard = sequelize.define("leaderboard", {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  teamname:{
    type: DataTypes.STRING(255),
    defaultValue:"TEAM",
    allowNull:false
  },
  event_id: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: { model: "events", key: "id" },
  },
  team_id: {
    type: DataTypes.STRING(255),
    allowNull: true,
    // type: DataTypes.INTEGER,
    // allowNull: false,
    unique:true
  },

  problem_1: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  problem_2: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  problem_3: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  problem_4: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  total_submissions: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  total_score: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  last_submission_time: {
    type: DataTypes.DATE,
    allowNull: true,
  },
  isjunior: {
    type: DataTypes.BOOLEAN,
    allowNull: false,
    defaultValue: false,
  }

}, {
  indexes: [
    {
      unique: true,
      fields: ["event_id", "team_id"], // ensures unique team per event
    },
  ],
  timestamps: true, // adds createdAt & updatedAt
});

module.exports = Leaderboard;
