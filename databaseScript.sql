-- Table to store person account info with additional profiling and important attributes
CREATE TABLE account
(
    accountId            INT AUTO_INCREMENT PRIMARY KEY,
    userName             VARCHAR(255) NULL,
    hashedPassword       VARCHAR(255) NULL,
    email                VARCHAR(255) NULL,
    bio                  VARCHAR(255) DEFAULT 'Welcome to stock4me!' NULL,
    profile              ENUM ('free', 'premium') NULL,
    status               ENUM ('valid', 'invalid') DEFAULT 'valid' NULL,
    createDateTime       TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    age                  INT NULL,
    sex                  ENUM('male', 'female', 'other') NULL,
    occupation           VARCHAR(255) NULL,
    incomeLevel          FLOAT NULL,
    netWorth             FLOAT NULL,
    investmentExperience ENUM('novice', 'intermediate', 'expert') NULL,
    riskTolerance        ENUM('low', 'medium', 'high') NULL,
    investmentGoals      VARCHAR(255) NULL
);

-- User Favourites List(watchList)
CREATE TABLE watchList(
    watchItemId INT AUTO_INCREMENT PRIMARY KEY,
    accountId    INT NOT NULL,
    stockSymbol  TEXT NOT NULL,
    addedDate    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
);
-- User preferences List(Industry,Country), input when they sign up
CREATE TABLE preferences
(
    preferencesId     INT AUTO_INCREMENT PRIMARY KEY,
    accountId    INT NOT NULL,
    preferenceIndustry     TEXT NOT NULL,
    preferenceCountry TEXT NOT NULL,
    addedDate    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
);

-- Table to store person follow someone
CREATE TABLE followList
(
    followId     INT AUTO_INCREMENT PRIMARY KEY,
    accountId    INT NOT NULL,
    followedId   INT NOT NULL,
    followDate   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId),
    FOREIGN KEY (followedId) REFERENCES account(accountId)
);

-- Table to store person search stock history
CREATE TABLE searchHistory
(
    searchId     INT AUTO_INCREMENT PRIMARY KEY,
    accountId    INT NOT NULL,
    stockSymbol  TEXT NOT NULL,
    searchDate   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
);

-- Merged table to store stock prediction history and results
CREATE TABLE predictionData
(
    predictionId      INT AUTO_INCREMENT PRIMARY KEY,
    stockSymbol       TEXT NOT NULL,
    requestDate       TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    minPredictedPrice FLOAT NULL,
    avgPredictedPrice FLOAT NULL,
    maxPredictedPrice FLOAT NULL,
    buyPercentage     FLOAT NULL,
    holdPercentage    FLOAT NULL,
    sellPercentage    FLOAT NULL
);


-- Table to store the recommendation based on personal interests
CREATE TABLE recommendationList
(
    recommendationId INT AUTO_INCREMENT PRIMARY KEY,
    accountId        INT NOT NULL,
    recommendedStock TEXT NOT NULL,
    recommendationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
);

-- Table to store user-specific thresholds for stock changes (Configuration; 5% change in stock price
CREATE TABLE thresholdSettings
(
    thresholdId    INT AUTO_INCREMENT PRIMARY KEY,
    accountId      INT NOT NULL,
    stockSymbol    TEXT NOT NULL,
    changePercentage FLOAT NOT NULL,
    notifyDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
);

-- Table to store user reviews of the product/website
CREATE TABLE review
(
    reviewId      INT AUTO_INCREMENT PRIMARY KEY,
    accountId     INT NOT NULL,
    rating        INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    reviewText    TEXT NULL,
    reviewDate    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
);

-- Table to store user comments on company stocks
CREATE TABLE comment
(
    commentId     INT AUTO_INCREMENT PRIMARY KEY,
    accountId     INT NOT NULL,
    stockSymbol   TEXT NOT NULL,
    commentText   TEXT NOT NULL,
    commentDate   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
);
CREATE TABLE emailVerification(
    verificationId INT AUTO_INCREMENT PRIMARY KEY ,
    verificationCode INT NOT NULL ,
    verificationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL
);
CREATE TABLE notification(
    notificationId INT AUTO_INCREMENT PRIMARY KEY ,
    accountId INT NOT NULL ,
    notification VARCHAR(255) NOT NULL DEFAULT 'Welcome to Stock Forecast4.me',
    notificationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL ,
    FOREIGN KEY (accountId) REFERENCES account(accountId)
)