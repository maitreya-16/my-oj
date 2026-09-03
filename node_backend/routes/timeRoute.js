const express = require('express');
require("dotenv").config();
const timeController = require("../controllers/timeController");
const auth = require('../middlewares/authMiddleware')
const router = express.Router();


// router.post("/register", userController.registerUser);
router.get("/", auth, timeController.getEventWithRemainingTime);

module.exports = router;

