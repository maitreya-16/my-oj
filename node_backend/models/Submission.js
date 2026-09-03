const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Submission = sequelize.define('submission', {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    team_id: {
        type: DataTypes.STRING(255),
        allowNull: true,
        // type: DataTypes.INTEGER,
        // allowNull: false
        //     references: {
        //         model: 'teams', // lowercase plural
        //         key: 'id'
        //     },

    },
      teamname:{
    type: DataTypes.STRING(255),
    defaultValue:"TEAM",
    allowNull:false
  },
    problem_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'problems', // lowercase plural
            key: 'id'
        },
    },
    event_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'events', // lowercase plural
            key: 'id'
        },
    },
    code: { type: DataTypes.TEXT, allowNull: false },
    language: { type: DataTypes.STRING, allowNull: false },
    failed_test_case: {
        type: DataTypes.TEXT,
        defaultValue: null,
        allowNull: true
    },
    result: {
        type: DataTypes.TEXT,
        allowNull: false,
        defaultValue: 'Pending'
    },
    score: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    },
    submitted_at: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    },
    verdict: { type: DataTypes.STRING, allowNull: true },
    created_at: { type: DataTypes.DATE, allowNull: true, defaultValue: DataTypes.NOW }
}, {
    timestamps: false
});
module.exports = Submission;
