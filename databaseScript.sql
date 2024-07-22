create table account
(
    accountId            int auto_increment
        primary key,
    userName             varchar(255)                                             null,
    hashedPassword       varchar(255)                                             null,
    email                varchar(255)                                             null,
    bio                  varchar(255)              default 'Welcome to stock4me!' null,
    profile              enum ('free', 'premium', 'admin')                        null,
    status               enum ('valid', 'invalid') default 'valid'                null,
    createDateTime       timestamp                 default CURRENT_TIMESTAMP      null,
    age                  int                                                      null,
    sex                  enum ('male', 'female', 'other')                         null,
    occupation           varchar(255)                                             null,
    incomeLevel          float                                                    null,
    netWorth             float                                                    null,
    investmentExperience enum ('novice', 'intermediate', 'expert')                null,
    riskTolerance        enum ('low', 'medium', 'high')                           null,
    investmentGoals      varchar(255)                                             null,
    isPrivateAccount     tinyint(1)                default 0                      not null,
    mlViewLeft           int                       default 10                     not null,
    apikey               varchar(255)                                             not null,
    card_number          varchar(255)                                             null,
    nextPaymentDate      datetime                                                 null
);

create table comment
(
    commentId   int auto_increment
        primary key,
    accountId   int                                 not null,
    stockSymbol text                                not null,
    commentText text                                not null,
    commentDate timestamp default CURRENT_TIMESTAMP null,
    likes       int       default 0                 not null,
    dislikes    int       default 0                 null,
    constraint comment_ibfk_1
        foreign key (accountId) references account (accountId)
);

create index accountId
    on comment (accountId);

create table emailverification
(
    verificationId   int auto_increment
        primary key,
    email            varchar(255)                        not null,
    code             int                                 not null,
    verificationDate timestamp default CURRENT_TIMESTAMP null
);

create table followlist
(
    followId   int auto_increment
        primary key,
    accountId  int                                 not null,
    followedId int                                 not null,
    notifyMe   tinyint(1)                          null,
    followDate timestamp default CURRENT_TIMESTAMP null,
    constraint followlist_ibfk_1
        foreign key (accountId) references account (accountId),
    constraint followlist_ibfk_2
        foreign key (followedId) references account (accountId)
);

create index accountId
    on followlist (accountId);

create index followedId
    on followlist (followedId);

create table notification
(
    notificationId   int auto_increment
        primary key,
    accountId        int                                                  not null,
    notification     varchar(255) default 'Welcome to Stock Forecast4.me' not null,
    notificationType varchar(255)                                         not null,
    referenceId      int                                                  null,
    symbol           varchar(255)                                         null,
    notificationDate timestamp    default CURRENT_TIMESTAMP               null,
    constraint unique_notification
        unique (accountId, notification, notificationType, symbol),
    constraint notification_ibfk_1
        foreign key (accountId) references account (accountId)
);

create table predictiondata
(
    predictionId      int auto_increment
        primary key,
    stockSymbol       text                                not null,
    requestDate       timestamp default CURRENT_TIMESTAMP null,
    minPredictedPrice float                               null,
    avgPredictedPrice float                               null,
    maxPredictedPrice float                               null,
    buyPercentage     float                               null,
    holdPercentage    float                               null,
    sellPercentage    float                               null,
    timeRange         int                                 null,
    target            varchar(255)                        null,
    accountId         int                                 null,
    model             varchar(255)                        null,
    rawData           longtext                            null,
    constraint predictiondata__fk
        foreign key (accountId) references account (accountId)
);

create table preferences
(
    preferencesId      int auto_increment
        primary key,
    accountId          int                                 not null,
    preferenceIndustry text                                not null,
    preferenceCountry  text                                not null,
    addedDate          timestamp default CURRENT_TIMESTAMP null,
    constraint preferences_pk
        unique (accountId),
    constraint preferences_ibfk_1
        foreign key (accountId) references account (accountId)
);

create table recommendationlist
(
    recommendationId   int auto_increment
        primary key,
    accountId          int                                 not null,
    recommendedStock   longtext                            not null,
    recommendationDate timestamp default CURRENT_TIMESTAMP null,
    constraint recommendationlist_pk
        unique (accountId),
    constraint recommendationlist_ibfk_1
        foreign key (accountId) references account (accountId)
);

create table review
(
    reviewId   int auto_increment
        primary key,
    accountId  int                                 not null,
    rating     float                               not null,
    reviewText text                                null,
    reviewDate timestamp default CURRENT_TIMESTAMP null,
    constraint unique_review_stock
        unique (accountId),
    constraint review_ibfk_1
        foreign key (accountId) references account (accountId),
    check (`rating` between 0 and 5)
);

create table searchhistory
(
    searchId    int auto_increment
        primary key,
    accountId   int                                 not null,
    stockSymbol varchar(255)                        not null,
    searchDate  timestamp default CURRENT_TIMESTAMP null,
    constraint unique_account_stock
        unique (accountId, stockSymbol),
    constraint searchhistory_ibfk_1
        foreign key (accountId) references account (accountId)
);

create table thresholdsettings
(
    thresholdId      int auto_increment
        primary key,
    accountId        int                                 not null,
    stockSymbol      varchar(255)                        not null,
    changePercentage float                               not null,
    notifyDateTime   timestamp default CURRENT_TIMESTAMP null,
    constraint unique_thresholdSettings_stock
        unique (accountId, stockSymbol),
    constraint thresholdsettings_ibfk_1
        foreign key (accountId) references account (accountId)
);

create table watchlist
(
    watchItemId int auto_increment
        primary key,
    accountId   int                                 not null,
    stockSymbol text                                not null,
    addedDate   timestamp default CURRENT_TIMESTAMP null,
    constraint watchlist_pk
        unique (accountId),
    constraint watchlist_ibfk_1
        foreign key (accountId) references account (accountId)
);


SET @accountId = 1;


START TRANSACTION;


DELETE FROM comment WHERE accountId = @accountId;
DELETE FROM followlist WHERE accountId = @accountId;
DELETE FROM notification WHERE accountId = @accountId;
DELETE FROM predictiondata WHERE accountId = @accountId;
DELETE FROM preferences WHERE accountId = @accountId;
DELETE FROM recommendationlist WHERE accountId = @accountId;
DELETE FROM review WHERE accountId = @accountId;
DELETE FROM searchhistory WHERE accountId = @accountId;
DELETE FROM thresholdsettings WHERE accountId = @accountId;
DELETE FROM watchlist WHERE accountId = @accountId;
DELETE FROM emailverification WHERE email IN (SELECT email FROM account WHERE accountId = @accountId);
DELETE FROM account WHERE accountId = @accountId;

COMMIT;

