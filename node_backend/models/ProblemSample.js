

const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const ProblemSample = sequelize.define('problemsample', {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    problem_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'problems', // lowercase plural
            key: 'id'
        }
    },
    input: { type: DataTypes.TEXT, allowNull: false },
    output: { type: DataTypes.TEXT, allowNull: false },
    explanation: { type: DataTypes.TEXT, allowNull: true }
}, {
    timestamps: false
});

module.exports = ProblemSample;
