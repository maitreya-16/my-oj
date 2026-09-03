const express = require("express");
require("dotenv").config();
// const cors = require("cors");
const sequelize = require("./config/database");
const { syncDB } = require('./models');
const cookieParser = require('cookie-parser');
const adminRoutes = require('./routes/adminRoutes');
const userRoutes = require('./routes/userRoutes');
const problemroutes = require('./routes/problemroutes');
const resultRoutes = require('./routes/resultRoutes');
const leaderboardRoutes = require('./routes/leaderboardroutes');
const submissionRoutes = require('./routes/submissionRoutes');
const webhookRoutes = require('./routes/WebhookRoutes');
const timeRoutes = require('./routes/timeRoute.js');
const app = express();
app.use(express.json());  // To handle JSON payloads
app.use(cookieParser())
//const PORT = process.env.PORT || 5000;
const cors = require("cors");
const auth = require("./middlewares/authMiddleware.js");

// CORS configuration
const allowedOrigins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://ctd-rc-frontend-2025.vercel.app",
    "https://ctd-rc.credenz.co.in",
    process.env.FLASK_API_BASE, 
    process.env.FRONTEND_URL,
  ];

// Allow all origins
app.use(cors({
  origin: allowedOrigins,
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true
}));

// Routes
app.get("/", (req, res) => res.send("🚀 Online Judge API is running..."));
app.use("/admin", adminRoutes);
app.use("/user", userRoutes);
app.use("/problems", problemroutes);
app.use("/result", resultRoutes);
app.use("/leaderboard", leaderboardRoutes);
app.use("/submission", submissionRoutes);
app.use("/webhook", webhookRoutes);
app.use("/time",timeRoutes);
app.get('/verify',auth,(req,res)=>{
  res.status(200).json({authenticated:true,user:req.user});  
});

const PORT = process.env.PORT || 3000;

syncDB().then(()=>{
  console.log("DB synced")
})

sequelize.sync()
  .then(() => {
    console.log("✅ Database connected & synced");
    app.listen(PORT, '0.0.0.0', () => {
      console.log(`🚀 Server running at http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("❌ Failed to connect DB:", err);
  });
