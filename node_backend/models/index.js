const sequelize = require('../config/database');
const User = require('./User');
// const Team = require('./Team'); // REMOVED
const Problem = require('./Problem');
const Submission = require('./Submission');
const ProblemSample = require('./ProblemSample');
const Event = require('./Event');
const Leaderboard = require('./Leaderboard');


// // User ↔ Event relationships
// User.belongsTo(Event, { foreignKey: 'event_id', as: 'Event' });
// Event.hasMany(User, { foreignKey: 'event_id', as: 'Users' });


// Submission.belongsTo(User, { foreignKey: 'team_id', targetKey: 'team_id', as: 'TeamUsers' });

// // Submission.belongsTo(User, { foreignKey: 'user_id', as: 'User' });
// // User.hasMany(Submission, { foreignKey: 'user_id', as: 'Submissions' });

// // Submission ↔ Problem relationships
// Submission.belongsTo(Problem, { foreignKey: 'problem_id', as: 'Problem' });
// Problem.hasMany(Submission, { foreignKey: 'problem_id', as: 'Submissions' });
Problem.belongsTo(Event, {
  foreignKey: "event_id",
  as: "event",
  onDelete: "RESTRICT",
  onUpdate: "CASCADE"   // keep cascade for updates
});

Event.hasMany(Problem, {
  foreignKey: "event_id",
  as: "problems",
  onDelete: "RESTRICT",
  onUpdate: "CASCADE"
});

// Problem ↔ ProblemSample relationships
Problem.hasMany(ProblemSample, {
  foreignKey: 'problem_id', 
  as: 'samples', 
  onDelete: "RESTRICT",
  onUpdate: "CASCADE"
});
ProblemSample.belongsTo(Problem, {
  foreignKey: 'problem_id',
  onDelete: "RESTRICT",
  onUpdate: "CASCADE"
});

// Problem ↔ Event relationships

// Submission ↔ Event relationships
// Submission.belongsTo(Event, { foreignKey: 'event_id', as: 'Event' });
// Event.hasMany(Submission, { foreignKey: 'event_id', as: 'Submissions' });

// Leaderboard ↔ Event relationships
// Leaderboard.belongsTo(Event, { foreignKey: 'event_id', as: 'Event' });
// Event.hasMany(Leaderboard, { foreignKey: 'event_id', as: 'Leaderboards' });

// User.js
// User.belongsTo(Leaderboard, { foreignKey: 'ncc', as: 'nccTeam' });
// User.belongsTo(Leaderboard, { foreignKey: 'rcc', as: 'rccTeam' });
// User.belongsTo(Leaderboard, { foreignKey: 'enigma', as: 'enigmaTeam' });

// // Leaderboard.js
// Leaderboard.hasMany(User, { foreignKey: 'ncc', as: 'nccUsers' });
// Leaderboard.hasMany(User, { foreignKey: 'rcc', as: 'rccUsers' });
// Leaderboard.hasMany(User, { foreignKey: 'enigma', as: 'enigmaUsers' });


const syncDB = async () => {
  try {
    await sequelize.sync({ alter: true });
    console.log("All models were synchronized successfully.");
  } catch (error) {
    console.error("Error syncing database models:", error);
  }
};

console.log("it is done");

module.exports = {
  sequelize,
  User,
  // Team, 
  Problem,
  Submission,
  ProblemSample,
  Event,
  Leaderboard,
  syncDB
};