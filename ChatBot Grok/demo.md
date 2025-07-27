
# URL Shortener App 🌐

A client-server application for shortening URLs with real-time click statistics tracking.

---

## 📂 Folder Structure
```tree
.
├── README.md
├── Screenshorts
│   ├── output1.png
│   ├── output2.png
│   ├── stats_after_clicking.png
│   └── stats_before_clicks.png
├── client
│   ├── .gitignore
│   ├── README.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package*.json
│   ├── public
│   │   └── vite.svg
│   ├── src
│   │   ├── App.jsx
│   │   ├── assets
│   │   │   └── react.svg
│   │   ├── components
│   │   │   ├── Statistics.jsx
│   │   │   └── UrlShortenerForm.jsx
│   │   └── main.jsx
│   └── vite.config.js
└── server
    ├── .gitignore
    ├── middleware
    │   └── logger.js
    ├── models
    │   └── urlStore.js
    ├── package*.json
    ├── routes
    │   └── urlRoutes.js
    └── server.js
```

---

## 🚀 Getting Started
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-repo/url-shortener.git
   cd url-shortener
   ```

2. **Install dependencies**  
   ```bash
   # Client-side (React/Vite)
   cd client
   npm install

   # Server-side (Node.js/Express)
   cd ../server
   npm install
   ```

3. **Run the app**  
   ```bash
   # Start client (localhost:3000)
   cd client && npm run dev &

   # Start server (localhost:3001)
   cd ../server && npm start
   ```

---

## 🛠️ Technologies Used
- **Frontend**: React, Vite, JSX
- **Backend**: Node.js, Express.js
- **Tools**: ESLint, Git, NPM

---

## 🧪 Scripts / Commands
- **Client**:  
  `npm run dev` (start development server)  
- **Server**:  
  `npm start` (start production server)  
  `npm run dev` (development mode with hot reload)

---

## 📄 License
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://choosealicense.com/licenses/mit/)  
Licensed under MIT. See `LICENSE` for details.

---

## 👤 Author
Developed by [Your Name Here]  
*Replace with your GitHub profile or team name*

---

## 🎯 Additional Notes
- **Live Demo**: [Coming Soon](#)  
- **Features**:  
  - Shorten URLs with custom slugs  
  - Real-time click tracking (see `Screenshorts/` for examples)  
  - REST API for URL management  
- **Contributions**: Pull requests welcome!
```

Key Observations:
1. The React frontend uses Vite (via `vite.config.js`)
2. Backend uses Express.js (from `server.js` and routes)
3. Click tracking is visualized in the `Screenshorts` folder
4. Clean separation of concerns between client/server folders
5. Uses modern JS/TS practices (ESLint config, package.json scripts)