const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

// FATAL 1: Hardcoded sensitive keys
const STRIPE_SECRET_KEY = "sk_live_this_is_a_mock_key_for_testing_purposes";
const DB_PASSWORD = "admin_super_password_999";

app.get('/', (req, res) => {
    res.send('Welcome to the vulnerable Node.js app!');
});

// FATAL 2: Command Injection
app.get('/ping', (req, res) => {
    const target = req.query.ip;
    if (!target) {
        return res.status(400).send("Provide an IP to ping");
    }
    
    // Attacker can pass "127.0.0.1; rm -rf /"
    exec(`ping -c 4 ${target}`, (error, stdout, stderr) => {
        if (error) {
            res.status(500).send(`Error: ${error.message}`);
            return;
        }
        res.send(`<pre>${stdout}</pre>`); // Also XSS via unsanitized output
    });
});

// FATAL 3: Arbitrary Code Execution via eval()
app.post('/calculate', (req, res) => {
    const mathExpression = req.body.expression;
    try {
        // Attacker can pass: "require('child_process').execSync('whoami')"
        const result = eval(mathExpression);
        res.send({ result });
    } catch (e) {
        res.status(500).send("Math error");
    }
});

// FATAL 4: Regex Denial of Service (ReDoS)
app.post('/validate-email', (req, res) => {
    const email = req.body.email;
    // Extremely inefficient regex that can cause catastrophic backtracking
    const regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    
    if (regex.test(email)) {
        res.send("Valid email");
    } else {
        res.send("Invalid email");
    }
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
