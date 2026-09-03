
const { Leaderboard, Team, Problem } = require("../models");
/**
 * Get leaderboard for an event
 * - Sorted by total_score (desc), then last_submission_time (asc)
 */
exports.getLeaderboard = async (req, res) => {
  try {
    // const { event_id } = req.params;
    const event_id = req.user.event_id;
    const isjunior = req.user.isjunior
    const leaderboard = await Leaderboard.findAll({
      where: { event_id ,isjunior},
      order: [
        ["total_score", "DESC"],
        ["last_submission_time", "ASC"], // tie-breaker ^_^
      ],
    });
    return res.status(200).json(leaderboard);
  } catch (error) {
    console.error("Error fetching leaderboard:", error);
    return res.status(500).json({ message: "Server error", error: error.message });
  }
};
