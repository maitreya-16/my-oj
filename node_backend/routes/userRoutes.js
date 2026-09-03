const express = require('express');
require("dotenv").config();
const userController = require("../controllers/userController");
const router = express.Router();

const auth = require('../middlewares/authMiddleware')

router.post("/register", userController.registerUser);
router.post("/updatepassword", userController.updatePassword);
router.post("/login", userController.Login);
router.post("/logout", auth, userController.Logout);
router.get('/profile', auth, userController.GetProfile);
router.get('/gethistory', auth, userController.gethistory);
module.exports = router;

