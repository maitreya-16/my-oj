const express = require("express");
const router = express.Router();
const leaderboardController = require("../controllers/leaderboardController");

const auth = require("../middlewares/authMiddleware");
// Get leaderboard for an event
router.get("/", auth, leaderboardController.getLeaderboard);

module.exports = router;

