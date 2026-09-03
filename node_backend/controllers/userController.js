const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { User, Team, Submission } = require("../models");
require("dotenv").config();
const Event = require("../models/Event");
const { v4: uuidv4 } = require('uuid');

exports.registerUser = async (req, res) => {
    try {
        console.log(req.body);

        const { teamname, username, password, isjunior, event_id } = req.body;

        // Basic validation
        if (!username || !password || isjunior === undefined) {
            return res.status(400).json({ error: 'Username, password and isjunior are required' });
        }

        if (typeof password !== 'string' || password.length < 6) {
            return res.status(400).json({ error: 'Password must be at least 6 characters long' });
        }

        // Optional: Check if event exists (only if you're actually using event_id)
        if (event_id) {
            const event = await Event.findByPk(event_id);
            if (!event) {
                return res.status(400).json({ error: 'Event not found' });
            }
        }

        // Check if user already exists
        const existingUser = await User.findOne({ where: { username } });
        if (existingUser) {
            return res.status(400).json({ error: 'Username already taken' });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const newUser = await User.create({
            username,
            teamname: teamname || "TEAM",
            password: hashedPassword,
            isjunior,
            role:"USER",
            rc:uuidv4()
        });

        res.status(201).json({
            message: 'User registered successfully!',
            user: {
                id: newUser.id,
                username: newUser.username,
                teamname: newUser.teamname,
                isjunior: newUser.isjunior,
                role: newUser.role
            }
        });

    } catch (error) {
        console.error('Registration error:', error);

        if (error.name === 'SequelizeValidationError') {
            return res.status(400).json({
                error: 'Validation error',
                details: error.errors.map(e => e.message)
            });
        }

        res.status(500).json({
            error: 'Error registering user',
            details: error.message
        });
    }
};

exports.updatePassword = async (req, res) => {
    try {
        const { username, newPassword } = req.body;

        // Validation
        if (!username || !newPassword) {
            return res.status(400).json({
                error: "Username and newPassword are required",
                received: req.body
            });
        }

        if (typeof newPassword !== "string" || newPassword.length < 6) {
            return res.status(400).json({
                error: "New password must be at least 6 characters long"
            });
        }

        // Find user
        const user = await User.findOne({ where: { username } });

        if (!user) {
            return res.status(404).json({
                error: "User not found"
            });
        }

        // Hash new password
        const hashedPassword = await bcrypt.hash(newPassword, 10);

        // Update password
        user.password = hashedPassword;
        await user.save();

        return res.status(200).json({
            message: "Password updated successfully"
        });

    } catch (error) {
        console.error("Update password error:", error);

        return res.status(500).json({
            error: "Error updating password",
            details: error.message
        });
    }
};


exports.Login = async (req, res) => {
    try {
        const {teamname, username, password, event_id, isjunior } = req.body;
        let isEnded = false;
        // Input validation
    if (!username || isjunior === undefined || !password || !event_id || !teamname) {
            return res.status(400).json({ error: 'Username,Password,Teamname and isjunior are required' });
        }

        const event = await Event.findByPk(event_id);
        if (!event) {
            return res.status(400).json({ error: 'Event not found' });
        }

        const now = new Date();
        if (!event.start_time || now < event.start_time) {
            return res.status(400).json({ error: "Event has not started yet" });
        }
        if (now > event.end_time) {
            // return res.status(501).json({ error: "Event has ended" });
            isEnded = true;
        }
        let user;

        user = await User.findOne({ where: { username,teamname } });

        if (user && user.isjunior != isjunior) {
            return res.status(400).json({ error: "User not found" });
        }

        if (!user || (event_id === 2 && user.rc === 0)) {
            return res.status(400).json({ error: "User not found. Please register first" });
        }
        const validPassword = await bcrypt.compare(password, user.password);

        if (!validPassword) {
            return res.status(400).json({ error: "Invalid username or password" });
        }

        const token = jwt.sign(
            {
                id: user.id,
                username: user.username,
                event_id: event_id,
                isjunior: user.isjunior,
                team_id: user.rc,
                teamname:user.teamname
            },
            process.env.JWT_SECRET,
            { expiresIn: "2h" }
        );

        // Get cookie settings from environment variables
        const domain = process.env.COOKIE_DOMAIN || 'localhost';
        const isSecure = process.env.COOKIE_SECURE === 'true';
        const sameSite = process.env.COOKIE_SAME_SITE || 'None';

        console.log('Cookie settings:', {
            domain,
            isSecure,
            sameSite,
            frontendUrl: process.env.FRONTEND_URL
        });

        res.cookie("token", token, {
            httpOnly: true,    // Prevents JavaScript access
            secure: true,  // Set via environment variable
            sameSite: "None", // Set via environment variable
            // domain: domain,    // Set domain based on environment
            path: '/',         // Cookie available for all paths
            maxAge: 2 * 60 * 60 * 1000, // 2 hours
            // credentials: 'include' // Required for cross-origin requests
        });

        console.log('Response headers:', res.getHeaders());
        if (isEnded) {
            return res.status(501).json({
                status: "ended", message: "Event has ended", user: {
                    isVerified:true,
                    username: user.username,
                    event_id: user.event_id,
                    isjunior: user.isjunior,
                    team_id: user.rc
                }
            });
        }
        return res.status(200).json({
            message: "Logged in successfully",
            isVerified:true,
            user: {
                username: user.username,
                event_id: user.event_id,
                isjunior: user.isjunior,
            }
        });

    } catch (error) {
        console.error("Error logging in:", error);
        res.status(400).json({ error: "Error logging in", details: error.message });
    }
};
exports.GetProfile = async (req, res) => {
    try {
        const user = await User.findByPk(req.user.id, { attributes: { exclude: ['password'] } });
        return res.status(200).json({ user });
    } catch (error) {
        console.error("Error fetching user profile:", error);
        res.status(500).json({ error: "Error fetching user profile", details: error.message });
    }
};

// exports.Logout = async (req,res)=>{
//     try{
//         res.clearCookie("token");
//         res.status(200).json({message:"User logged out successfully"});
//     }
//     catch(error){
//         console.error("Error logging out:", error);
//         res.status(500).json({ error: "Error logging out", details: error.message });
//     }
// };

exports.Logout = async (req, res) => {
    try {
        res.clearCookie("token", {
            httpOnly: true,
            sameSite: "None",
            secure: true,
            path: '/'   // must match how you set it!
        });
        return res.status(200).json({ message: "User logged out successfully" });
    }
    catch (error) {
        console.error("Error logging out:", error);
        res.status(500).json({ error: "Error logging out", details: error.message });
    }
};

exports.gethistory = async (req, res) => {
    try {
        const team_id = req.user.team_id;
        const submissions = await Submission.findAll({
            where: { team_id },
            order: [['submitted_at', 'DESC']]
        });
        res.status(200).json(submissions);
    }
    catch (error) {
        res.status(500).json({ error: 'Error fetching submission history', details: error.message });
    }
};
