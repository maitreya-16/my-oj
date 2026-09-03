const express = require("express");
const router = express.Router();
const resultController = require("../controllers/resultcontroller");
const auth = require("../middlewares/authMiddleware");
// Get result (rank + stats) of a particular team in an event
router.get("/", auth, resultController.getTeamResult);

module.exports = router;
