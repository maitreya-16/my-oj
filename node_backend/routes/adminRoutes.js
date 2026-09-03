const express = require("express");
const adminAuth= require("../middlewares/adminMiddleware");
const multer = require("multer"); // Make sure this is correctly imported
const fs = require("fs");
const path = require("path");
const router = express.Router();

const adminController = require("../controllers/adminController");

router.post("/register", adminController.registerAdmin);
router.post("/login", adminController.loginAdmin);
router.get("/problems", adminAuth, adminController.getAllProblems);
router.get("/users", adminAuth, adminController.getAllUsers);

router.get("/teams", adminAuth, adminController.getAllTeams);


router.post("/create-event", adminAuth, adminController.createEvent);

router.get("/problems", adminAuth, adminController.getAllProblems);
module.exports = router;

