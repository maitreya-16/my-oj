const { DataTypes } = require("sequelize");
const sequelize = require("../config/database");

const Problem = sequelize.define(
  "problem",
  {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    title: { type: DataTypes.STRING, allowNull: false },
    description: { type: DataTypes.TEXT, allowNull: false },
    score: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 50,
    },
    input_format: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    output_format: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    constraints: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    isjunior: {
      type: DataTypes.BOOLEAN,
      defaultValue:false,
      allowNull: false,
    },
    time_limit: {
      type: DataTypes.INTEGER,
      defaultValue: 2,
    },
    memory_limit: {
      type: DataTypes.INTEGER,
      defaultValue: 256,
    },
    event_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: "events", // lowercase plural
        key: "id",
      },
    },
  },
  {
    timestamps: false,
  }
);

module.exports = Problem;
