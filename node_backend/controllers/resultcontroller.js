const Leaderboard = require("../models/Leaderboard.js");
const sequelize = require("../config/database.js");


exports.getTeamResult = async (req, res) => {
  try {
    const event_id = req.user.event_id;
    const team_id = req.user.team_id;
    const isjunior = req.user.isjunior;

    if (!event_id || !team_id) {
      return res.status(400).json({ message: "Missing event_id or team_id in user data." });
    }

  
    const leaderboard = await Leaderboard.findAll({
      where: { event_id ,isjunior},
      order: [
        ["total_score", "DESC"],
        ["last_submission_time", "ASC"], 
      ],
    });

    if (!leaderboard.length) {
      return res.status(404).json({ message: "No leaderboard data for this event." });
    }

    let teamResult = null;
    let rank = null;

    leaderboard.forEach((entry, index) => {
      if (entry.team_id === team_id) {
        teamResult = entry;
        rank = index + 1; // rank starts at 1
      }
    });

    if (!teamResult) {
      return res.status(404).json({ message: "Team not found in this event." });
    }

    const solvedRows = await sequelize.query(
      `
      SELECT COUNT(s.problem_id) AS solved_count
      FROM problems p
      LEFT JOIN submissions s
        ON p.id = s.problem_id
       AND s.team_id = :team_id
       AND s.event_id = :event_id
       AND s.result = 'accepted'
      WHERE p.event_id = :event_id
        AND p.isjunior = :isjunior;
      `,
      {
        replacements: { team_id, event_id, isjunior },
        type: sequelize.QueryTypes.SELECT,
      }
    );

    const solved_count = solvedRows[0].solved_count || 0;

    const accuracy =
      teamResult.total_submissions > 0
        ? (solved_count / teamResult.total_submissions) * 100
        : 0;

    return res.status(200).json({
      teamname:teamResult.teamname,
      isjunior: teamResult.isjunior,
      rank: rank,
      total_score: teamResult.total_score,
      total_submissions: teamResult.total_submissions,
      problems_solved: solved_count,
      accuracy: `${accuracy.toFixed(2)}%`, 
    });
  } catch (error) {
    console.error("Error fetching team result:", error);
    return res.status(500).json({ message: "Server error", error: error.message });
  }
};
