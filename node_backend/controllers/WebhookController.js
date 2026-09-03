const Submission = require("../models/Submission.js");
const Leaderboard = require("../models/Leaderboard.js");
// const { where } = require("sequelize");
const { sendEvent } = require('./sse');

async function updateDatabase(submission_id, status, message, failed_test_case, score) {
  // Update submission
  const [affectedCount, [updatedSubmission]] = await Submission.update(
    { score, failed_test_case, result: status, verdict: message },
    { where: { id: submission_id }, returning: true }
  );

  if (affectedCount === 0 || !updatedSubmission) {
    console.log("Failed to get submission");
    return;
  }

  const problem_id = updatedSubmission.problem_id;
  const problemID = `problem_${problem_id%4===0?4:problem_id%4}`;
  const team_id = updatedSubmission.team_id;
  const event_id = updatedSubmission.event_id;
  
  // Find or create leaderboard entry
  let leaderboardEntry = await Leaderboard.findOne({ 
    where: { team_id: team_id }
  });

  if (!leaderboardEntry) {
    console.log("Creating new leaderboard entry for team:", team_id);
    leaderboardEntry = await Leaderboard.create({
      team_id,
      teamname:updatedSubmission.teamname,
      event_id,
      problem_1: 0,
      problem_2: 0,
      problem_3: 0,
      problem_4: 0,
      total_score: 0,
      total_submissions: 0,
      last_submission_time: new Date()
    });
  }

  // Update leaderboard if new score is higher
  if ((leaderboardEntry[problemID] || 0) < score) {
    const previousScore = leaderboardEntry[problemID] || 0;
    leaderboardEntry[problemID] = score;
    leaderboardEntry.last_submission_time = new Date();
    leaderboardEntry.total_score = leaderboardEntry.total_score + (score - previousScore);
  }
  leaderboardEntry.total_submissions = (leaderboardEntry.total_submissions +1 );
  await leaderboardEntry.save();
  return;
}


exports.RunWebhook = async (req, res) => {
  try {
    const { submission_id, status, message, user_output } = req.body;

    if (!submission_id || !status) {
      console.warn("[RunWebhook] Missing required fields:", req.body);
      return res
        .status(400)
        .json({ error: "submission_id and status are required" });
    }

    console.info(
      `[RunWebhook] Submission: ${submission_id}, Status: ${status}`
    );
    if (status !== "executed_successfully") {
      console.warn(`[RunWebhook] Message: ${message || "No message provided"}`);
    }

    console.log(req.body);

    // getIO().to(String(submission_id)).emit("result", {
    //   type: "run",
    //   submission_id,
    //   status,
    //   message,
    //   user_output,
    //   timestamp: new Date().toISOString(),
    // });

    sendEvent(submission_id, { status, message, user_output });

    return res
      .status(200)
      .json({ success: true, message: "Run webhook processed successfully" });
  } catch (error) {
    console.error("[RunWebhook] Error processing webhook:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
};

exports.SystemWebhook = async (req, res) => {
  try {
    const { submission_id, status, message, expected_output,user_output } = req.body;

    console.log(`System Webhook for ${submission_id} — ${status}`);
    if (status !== "executed_successfully") console.log(`Message: ${message}`);

    // getIO().to(String(submission_id)).emit("result", {
    //   type: "system",
    //   submission_id,
    //   user_output,
    //   status,
    //   message,
    //   expected_output,
    // });

    sendEvent(submission_id, { status, message, expected_output, user_output });

    res.status(200).json({ message: "System webhook processed successfully." });
  } catch (error) {
    console.error("Error processing system webhook:", error);
    res.status(500).json({ message: "Internal server error." });
  }
};

exports.SubmitWebhook = async (req, res) => {
  try {
    console.log(req.body);
    const { submission_id, status, message, total_test_case, failed_test_case, score } =
      req.body;

    if (!submission_id || !status) {
      console.warn("[SubmitWebhook] Missing required fields:", req.body);
      return res
        .status(400)
        .json({ error: "submission_id and status are required" });
    }

    const response = await updateDatabase(
      submission_id,
      status,
      message,
      failed_test_case,
      score
    );

    // getIO().to(String(submission_id)).emit("result", {
    //   type: "submit",
    //   submission_id,
    //   status,
    //   message,
    //   score,
    //   total_test_case,
    //   failed_test_case,
    //   timestamp: new Date().toISOString(),
    // });

    sendEvent(String(submission_id), { status, message, score, total_test_case, failed_test_case });

    return res
      .status(200)
      .json({
        success: true,
        message: "Submit webhook processed successfully",
      });
  } catch (error) {
    console.error("[SubmitWebhook] Error processing webhook:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
};
