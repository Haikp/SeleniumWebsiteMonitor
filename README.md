> This bot was requested to be made by a friend

# NFT Mint Monitoring Bot (Selenium + MetaMask)

This is a browser automation bot built using **Python and Selenium** to monitor live minting activity on the a deprecated platform. It automated user behavior by watching JavaScript DOM variables, interacting with the MetaMask browser extension, and attempting mint transactions when specific conditions were met. This bot was made a while ago, and I stopped updating it when the site it was used for went down. The bot was functional and served its purpose, however its fairly limited to working on just the particular site that I was using it on. In my situation the bot had to be tuned exactly to the website itself, which is why I didn't mind hard coding the XPaths to find what I needed to click or interact with.

This bot uses chrome profiles to function properly, which theres nothing wrong with it, but the folder organization needs to change as profiles are littered in the starting directory. I don't think I'll ever revisit this bot in particular though, but I will make a better organization system if I need to make another bot. I did not upload the chrome profiles to this repo.

Although it’s now deprecated, this project demonstrates:

- **Advanced Selenium usage** (handling stale elements, cross-tab navigation, session persistence)
- **Real-world automation scenarios** involving browser extensions
- **Testing resilience and monitoring logic** under real-time changes
- **Practical understanding of UI and backend integration triggers**

> Note: This project is archived. The target site has been discontinued, but the architecture remains useful for real-time DOM monitoring, browser automation, and end-to-end Selenium workflows.

## Features

- **Real-Time Monitoring**  
  Continuously tracks updates on the NFT mint activity page by inspecting DOM elements tied to mint/supply counters.

- **Automated Interaction**  
  Automates login into **MetaMask** (via the Chrome extension), confirms wallet actions, and clicks mint buttons when conditions are met.

- **DOM Condition Triggers**  
  Triggers actions based on:
  - Minted/supply ratio
  - New addresses on the transaction table
  - Presence of "refund" transactions

- **Browser Session Management**  
  - Automatically restarts the browser every X hours to avoid memory buildup.
  - Manages cookies, session state, and error recovery (e.g., `StaleElementReferenceException`, `TimeoutException`).

## Technologies Used

| Tool/Library               | Purpose                                 |
|---------------------------|-----------------------------------------|
| `Selenium` (Python)       | Browser automation                      |
| `ChromeDriver`            | Headless browser backend                |
| `MetaMask` Extension      | Wallet integration and Web3 interaction |
| `psutil`                  | (Optional) Runtime stats or process control |
| `XPath` / CSS Selectors   | Precise DOM targeting                   |

## Example Workflow (No Longer Functional)

1. Launch headless Chrome browser with MetaMask pre-installed.
2. Log in to MetaMask using a stored password.
3. Open activity page of site.
4. Monitor `minted / supply` values and look for new refundable transactions.
5. If minting conditions are met, switch to the mint page and:
   - Click the "Mint" button
   - Switch to MetaMask to confirm the transaction
6. Loop, refresh, and restart every N hours for stability.
