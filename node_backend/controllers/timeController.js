// controllers/eventController.js
const Event = require("../models/Event");

// Helper to format remaining time
function formatRemainingTime(ms) {
  if (ms <= 0) return "Event Ended";

  const seconds = Math.floor(ms / 1000) % 60;
  const minutes = Math.floor(ms / (1000 * 60)) % 60;
  const hours = Math.floor(ms / (1000 * 60 * 60)) % 24;
  const days = Math.floor(ms / (1000 * 60 * 60 * 24));

  return `${days}d ${hours}h ${minutes}m ${seconds}s`;
}

exports.getEventWithRemainingTime = async (req, res) => {
  try {
    const { event_id } = req.user;

    // Fetch event from DB
    const event = await Event.findByPk(event_id);

    if (!event) {
      return res.status(404).json({ message: "Event not found" });
    }

    const now = new Date();
    const endTime = new Date(event.end_time);
    const remainingMs = endTime - now;

    const remaining_time = formatRemainingTime(remainingMs);

    res.json({
      id: event.id,
      name: event.name,
      start_time: event.start_time,
      end_time: event.end_time,
      remainingMs,
      is_active: event.is_active,
      remaining_time, // formatted remaining time
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
};
