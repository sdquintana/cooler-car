ALTER USER 'root'@'%'  IDENTIFIED WITH mysql_native_password BY 'root';

use cooler_car;

-- tables
-- Table: CAT_BRANCH_OFFICE
CREATE TABLE CAT_BRANCH_OFFICE (
    branch_office_id int NOT NULL,
    branch_code varchar(12) NOT NULL,
    UNIQUE INDEX CAT_BRANCH_OFFICE_ak_1 (branch_code),
    CONSTRAINT CAT_BRANCH_OFFICE_pk PRIMARY KEY (branch_office_id)
);

-- Table: CAT_CAR
CREATE TABLE CAT_CAR (
    car_id int NOT NULL,
    CONSTRAINT CAT_CAR_pk PRIMARY KEY (car_id)
);

-- Table: CAT_CREDIT_CARD
CREATE TABLE CAT_CREDIT_CARD (
    credit_card_id int NOT NULL,
    number varchar(16) NOT NULL,
    expiry_date varchar(5) NOT NULL,
    CONSTRAINT CAT_CREDIT_CARD_pk PRIMARY KEY (credit_card_id)
);

-- Table: CAT_PAYMENT_METHOD
CREATE TABLE CAT_PAYMENT_METHOD (
    payment_method_id int NOT NULL,
    payment_method_type_id int NOT NULL,
    CONSTRAINT CAT_PAYMENT_METHOD_pk PRIMARY KEY (payment_method_id)
);

-- Table: CAT_PAYPAL_ACCOUNT
CREATE TABLE CAT_PAYPAL_ACCOUNT (
    paypal_account_id int NOT NULL,
    email varchar(72) NOT NULL,
    password varchar(72) NOT NULL,
    CONSTRAINT CAT_PAYPAL_ACCOUNT_pk PRIMARY KEY (paypal_account_id)
);

-- Table: CAT_PERSON
CREATE TABLE CAT_PERSON (
    person_id int NOT NULL,
    CONSTRAINT CAT_PERSON_pk PRIMARY KEY (person_id)
);

-- Table: CAT_RENT
CREATE TABLE CAT_RENT (
    trip_id int NOT NULL,
    number varchar(16) NOT NULL,
    CONSTRAINT CAT_RENT_pk PRIMARY KEY (trip_id)
);

-- Table: CAT_USER
CREATE TABLE CAT_USER (
    user_id int NOT NULL,
    email Varchar(72) NOT NULL,
    UNIQUE INDEX email_unique_constraint (email),
    CONSTRAINT CAT_USER_pk PRIMARY KEY (user_id)
);

-- Table: HIST_BRANCH_OFFICE
CREATE TABLE HIST_BRANCH_OFFICE (
    branch_office_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    name varchar(96) NOT NULL,
    address_1 varchar(96) NOT NULL,
    address_2 varchar(96) NOT NULL,
    cp varchar(8) NOT NULL,
    city varchar(96) NOT NULL,
    state varchar(96) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT HIST_BRANCH_OFFICE_pk PRIMARY KEY (branch_office_id,hash_key)
);

-- Table: HIST_CAR
CREATE TABLE HIST_CAR (
    car_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    motor_type_id int NOT NULL,
    trade_mark_type_id int NOT NULL,
    car_type_id int NOT NULL,
    niv varchar(96) NOT NULL,
    year int NOT NULL,
    model varchar(96) NOT NULL,
    expedition int NOT NULL,
    capacity int NOT NULL,
    user_id int NOT NULL,
    branch_office_id int NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT HIST_CAR_pk PRIMARY KEY (car_id,hash_key)
);

-- Table: HIST_PERSON
CREATE TABLE HIST_PERSON (
    person_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    user_id int NOT NULL,
    name varchar(96) NOT NULL,
    second_name varchar(96) NULL,
    last_name varchar(96) NOT NULL,
    second_last_name varchar(96) NULL,
    curp varchar(16) NULL,
    rfc varchar(13) NOT NULL,
    ine_number varchar(24) NULL,
    person_type_id int NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT HIST_PERSON_pk PRIMARY KEY (person_id,hash_key)
);

-- Table: HIST_USER
CREATE TABLE HIST_USER (
    user_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    password varchar(32) NOT NULL,
    phone varchar(12) NOT NULL,
    user_type_id int NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT HIST_USER_pk PRIMARY KEY (user_id,hash_key)
);

-- Table: LU_CAR_TYPE
CREATE TABLE LU_CAR_TYPE (
    car_type_id int NOT NULL,
    code varchar(12) NOT NULL,
    description_us varchar(144) NOT NULL,
    description_es varchar(144) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT LU_CAR_TYPE_pk PRIMARY KEY (car_type_id)
);

-- Table: LU_MOTOR_TYPE
CREATE TABLE LU_MOTOR_TYPE (
    motor_type_id int NOT NULL,
    code varchar(12) NOT NULL,
    description_us varchar(144) NOT NULL,
    description_es varchar(144) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT LU_MOTOR_TYPE_pk PRIMARY KEY (motor_type_id)
);

-- Table: LU_PAYMENT_METHOD_TYPE
CREATE TABLE LU_PAYMENT_METHOD_TYPE (
    payment_method_type_id int NOT NULL,
    code varchar(12) NOT NULL,
    description_us varchar(144) NOT NULL,
    description_es varchar(144) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT LU_PAYMENT_METHOD_TYPE_pk PRIMARY KEY (payment_method_type_id)
);

-- Table: LU_PERSON_TYPE
CREATE TABLE LU_PERSON_TYPE (
    person_type_id int NOT NULL,
    code varchar(12) NOT NULL,
    description_us varchar(144) NOT NULL,
    description_es varchar(144) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT LU_PERSON_TYPE_pk PRIMARY KEY (person_type_id)
);

-- Table: LU_TRADE_MARK_TYPE
CREATE TABLE LU_TRADE_MARK_TYPE (
    trade_mark_type_id int NOT NULL,
    code varchar(96) NOT NULL,
    description_us varchar(144) NOT NULL,
    description_es varchar(144) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT LU_TRADE_MARK_TYPE_pk PRIMARY KEY (trade_mark_type_id)
);

-- Table: LU_USER_TYPE
CREATE TABLE LU_USER_TYPE (
    user_type_id int NOT NULL,
    code varchar(12) NOT NULL,
    description_us varchar(144) NOT NULL,
    description_es varchar(144) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT LU_USER_TYPE_pk PRIMARY KEY (user_type_id)
);

-- Table: REL_CREDIT_CARD
CREATE TABLE REL_CREDIT_CARD (
    payment_method_id int NOT NULL,
    credit_card_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT REL_CREDIT_CARD_pk PRIMARY KEY (payment_method_id,credit_card_id)
);

-- Table: REL_PAYMENT_METHOD
CREATE TABLE REL_PAYMENT_METHOD (
    wallet_id int NOT NULL,
    payment_method_id int NOT NULL,
    user_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    principal bool NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT REL_PAYMENT_METHOD_pk PRIMARY KEY (wallet_id,hash_key)
);

-- Table: REL_PAYPAL_ACCOUNT
CREATE TABLE REL_PAYPAL_ACCOUNT (
    payment_method_id int NOT NULL,
    paypal_account_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT REL_PAYPAL_ACCOUNT_pk PRIMARY KEY (payment_method_id,paypal_account_id)
);

-- Table: REL_USER_RENT
CREATE TABLE REL_USER_RENT (
    trip_id int NOT NULL,
    user_id int NOT NULL,
    hash_key varchar(96) NOT NULL,
    rental_date date NOT NULL,
    delivery_date date NOT NULL,
    branch_office_id int NOT NULL,
    payment_method_id int NOT NULL,
    fare decimal(14,8) NOT NULL,
    damage_fee decimal(14,8) NOT NULL,
    car_id int NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active bool NOT NULL DEFAULT true,
    CONSTRAINT REL_USER_RENT_pk PRIMARY KEY (trip_id,user_id,hash_key)
);

-- foreign keys
-- Reference: CAT_CAR_LU_CAR_TYPE (table: HIST_CAR)
ALTER TABLE HIST_CAR ADD CONSTRAINT CAT_CAR_LU_CAR_TYPE FOREIGN KEY CAT_CAR_LU_CAR_TYPE (car_type_id)
    REFERENCES LU_CAR_TYPE (car_type_id);

-- Reference: CAT_CAR_LU_MODEL_TYPE (table: HIST_CAR)
ALTER TABLE HIST_CAR ADD CONSTRAINT CAT_CAR_LU_MODEL_TYPE FOREIGN KEY CAT_CAR_LU_MODEL_TYPE (trade_mark_type_id)
    REFERENCES LU_TRADE_MARK_TYPE (trade_mark_type_id);

-- Reference: CAT_CAR_LU_MOTOR_TYPE (table: HIST_CAR)
ALTER TABLE HIST_CAR ADD CONSTRAINT CAT_CAR_LU_MOTOR_TYPE FOREIGN KEY CAT_CAR_LU_MOTOR_TYPE (motor_type_id)
    REFERENCES LU_MOTOR_TYPE (motor_type_id);

-- Reference: CAT_PAYMENT_METHOD_LU_PAYMENT_METHOD_TYPE (table: CAT_PAYMENT_METHOD)
ALTER TABLE CAT_PAYMENT_METHOD ADD CONSTRAINT CAT_PAYMENT_METHOD_LU_PAYMENT_METHOD_TYPE FOREIGN KEY CAT_PAYMENT_METHOD_LU_PAYMENT_METHOD_TYPE (payment_method_type_id)
    REFERENCES LU_PAYMENT_METHOD_TYPE (payment_method_type_id);

-- Reference: HIST_BRANCH_OFFICE_CAT_BRANCH_OFFICE (table: HIST_BRANCH_OFFICE)
ALTER TABLE HIST_BRANCH_OFFICE ADD CONSTRAINT HIST_BRANCH_OFFICE_CAT_BRANCH_OFFICE FOREIGN KEY HIST_BRANCH_OFFICE_CAT_BRANCH_OFFICE (branch_office_id)
    REFERENCES CAT_BRANCH_OFFICE (branch_office_id);

-- Reference: HIST_CAR_CAT_BRANCH_OFFICE (table: HIST_CAR)
ALTER TABLE HIST_CAR ADD CONSTRAINT HIST_CAR_CAT_BRANCH_OFFICE FOREIGN KEY HIST_CAR_CAT_BRANCH_OFFICE (branch_office_id)
    REFERENCES CAT_BRANCH_OFFICE (branch_office_id);

-- Reference: HIST_CAR_CAT_CAR (table: HIST_CAR)
ALTER TABLE HIST_CAR ADD CONSTRAINT HIST_CAR_CAT_CAR FOREIGN KEY HIST_CAR_CAT_CAR (car_id)
    REFERENCES CAT_CAR (car_id);

-- Reference: HIST_CAR_CAT_USER (table: HIST_CAR)
ALTER TABLE HIST_CAR ADD CONSTRAINT HIST_CAR_CAT_USER FOREIGN KEY HIST_CAR_CAT_USER (user_id)
    REFERENCES CAT_USER (user_id);

-- Reference: HIST_PERSON_CAT_PERSON (table: HIST_PERSON)
ALTER TABLE HIST_PERSON ADD CONSTRAINT HIST_PERSON_CAT_PERSON FOREIGN KEY HIST_PERSON_CAT_PERSON (person_id)
    REFERENCES CAT_PERSON (person_id);

-- Reference: HIST_PERSON_CAT_USER (table: HIST_PERSON)
ALTER TABLE HIST_PERSON ADD CONSTRAINT HIST_PERSON_CAT_USER FOREIGN KEY HIST_PERSON_CAT_USER (user_id)
    REFERENCES CAT_USER (user_id);

-- Reference: HIST_PERSON_LU_PERSON_TYPE (table: HIST_PERSON)
ALTER TABLE HIST_PERSON ADD CONSTRAINT HIST_PERSON_LU_PERSON_TYPE FOREIGN KEY HIST_PERSON_LU_PERSON_TYPE (person_type_id)
    REFERENCES LU_PERSON_TYPE (person_type_id);

-- Reference: HIST_TRIP_CAT_TRIP (table: REL_USER_RENT)
ALTER TABLE REL_USER_RENT ADD CONSTRAINT HIST_TRIP_CAT_TRIP FOREIGN KEY HIST_TRIP_CAT_TRIP (trip_id)
    REFERENCES CAT_RENT (trip_id);

-- Reference: HIST_TRIP_CAT_USER (table: REL_USER_RENT)
ALTER TABLE REL_USER_RENT ADD CONSTRAINT HIST_TRIP_CAT_USER FOREIGN KEY HIST_TRIP_CAT_USER (user_id)
    REFERENCES CAT_USER (user_id);

-- Reference: HIST_USER_CAT_USER (table: HIST_USER)
ALTER TABLE HIST_USER ADD CONSTRAINT HIST_USER_CAT_USER FOREIGN KEY HIST_USER_CAT_USER (user_id)
    REFERENCES CAT_USER (user_id);

-- Reference: HIST_USER_LU_USER_TYPE (table: HIST_USER)
ALTER TABLE HIST_USER ADD CONSTRAINT HIST_USER_LU_USER_TYPE FOREIGN KEY HIST_USER_LU_USER_TYPE (user_type_id)
    REFERENCES LU_USER_TYPE (user_type_id);

-- Reference: REL_CREDIT_CAR_CAT_CREDIT_CARD (table: REL_CREDIT_CARD)
ALTER TABLE REL_CREDIT_CARD ADD CONSTRAINT REL_CREDIT_CAR_CAT_CREDIT_CARD FOREIGN KEY REL_CREDIT_CAR_CAT_CREDIT_CARD (credit_card_id)
    REFERENCES CAT_CREDIT_CARD (credit_card_id);

-- Reference: REL_CREDIT_CAR_CAT_PAYMENT_METHOD (table: REL_CREDIT_CARD)
ALTER TABLE REL_CREDIT_CARD ADD CONSTRAINT REL_CREDIT_CAR_CAT_PAYMENT_METHOD FOREIGN KEY REL_CREDIT_CAR_CAT_PAYMENT_METHOD (payment_method_id)
    REFERENCES CAT_PAYMENT_METHOD (payment_method_id);

-- Reference: REL_PAYMENT_METHOD_CAT_PAYMENT_METHOD (table: REL_PAYMENT_METHOD)
ALTER TABLE REL_PAYMENT_METHOD ADD CONSTRAINT REL_PAYMENT_METHOD_CAT_PAYMENT_METHOD FOREIGN KEY REL_PAYMENT_METHOD_CAT_PAYMENT_METHOD (payment_method_id)
    REFERENCES CAT_PAYMENT_METHOD (payment_method_id);

-- Reference: REL_PAYMENT_METHOD_CAT_USER (table: REL_PAYMENT_METHOD)
ALTER TABLE REL_PAYMENT_METHOD ADD CONSTRAINT REL_PAYMENT_METHOD_CAT_USER FOREIGN KEY REL_PAYMENT_METHOD_CAT_USER (user_id)
    REFERENCES CAT_USER (user_id);

-- Reference: REL_PAYPAL_ACCOUNT_CAT_PAYMENT_METHOD (table: REL_PAYPAL_ACCOUNT)
ALTER TABLE REL_PAYPAL_ACCOUNT ADD CONSTRAINT REL_PAYPAL_ACCOUNT_CAT_PAYMENT_METHOD FOREIGN KEY REL_PAYPAL_ACCOUNT_CAT_PAYMENT_METHOD (payment_method_id)
    REFERENCES CAT_PAYMENT_METHOD (payment_method_id);

-- Reference: REL_PAYPAL_ACCOUNT_CAT_PAYPAL_ACCOUNT (table: REL_PAYPAL_ACCOUNT)
ALTER TABLE REL_PAYPAL_ACCOUNT ADD CONSTRAINT REL_PAYPAL_ACCOUNT_CAT_PAYPAL_ACCOUNT FOREIGN KEY REL_PAYPAL_ACCOUNT_CAT_PAYPAL_ACCOUNT (paypal_account_id)
    REFERENCES CAT_PAYPAL_ACCOUNT (paypal_account_id);

-- Reference: REL_USER_RENT_CAT_BRANCH_OFFICE (table: REL_USER_RENT)
ALTER TABLE REL_USER_RENT ADD CONSTRAINT REL_USER_RENT_CAT_BRANCH_OFFICE FOREIGN KEY REL_USER_RENT_CAT_BRANCH_OFFICE (branch_office_id)
    REFERENCES CAT_BRANCH_OFFICE (branch_office_id);

-- Reference: REL_USER_RENT_CAT_CAR (table: REL_USER_RENT)
ALTER TABLE REL_USER_RENT ADD CONSTRAINT REL_USER_RENT_CAT_CAR FOREIGN KEY REL_USER_RENT_CAT_CAR (car_id)
    REFERENCES CAT_CAR (car_id);

-- Reference: REL_USER_TRIP_CAT_PAYMENT_METHOD (table: REL_USER_RENT)
ALTER TABLE REL_USER_RENT ADD CONSTRAINT REL_USER_TRIP_CAT_PAYMENT_METHOD FOREIGN KEY REL_USER_TRIP_CAT_PAYMENT_METHOD (payment_method_id)
    REFERENCES CAT_PAYMENT_METHOD (payment_method_id);

-- End of file.

CREATE DATABASE dim;

USE dim;

-- AUTO-GENERATED DEFINITION
CREATE TABLE DIM_BRANCH_OFFICE
(
    BRANCH_OFFICE_ID           INT         NOT NULL,
    BRANCH_OFFICE_CODE         VARCHAR(12) NOT NULL,
    BRANCH_OFFICE_NAME         VARCHAR(96) NOT NULL,
    BRANCH_OFFICE_ADDRESS_1    VARCHAR(96) NOT NULL,
    BRANCH_OFFICE_ADDRESS_2    VARCHAR(96) NOT NULL,
    BRANCH_OFFICE_ADDRESS_CITY VARCHAR(96) NOT NULL,
    BRANCH_OFFICE_CP           VARCHAR(8)  NOT NULL,
    BRANCH_OFFICE_STATE        VARCHAR(96) NOT NULL
);


-- AUTO-GENERATED DEFINITION
CREATE TABLE DIM_CAR
(
    CAR_ID                    INT          NOT NULL,
    HASH_KEY                  VARCHAR(96)  NOT NULL,
    MOTOR_CODE                VARCHAR(12)  NOT NULL,
    MOTOR_DESCRIPTION_ES      VARCHAR(144) NOT NULL,
    TRADE_MARK_CODE           VARCHAR(96)  NOT NULL,
    TRADE_MARK_DESCRIPTION_ES VARCHAR(144) NOT NULL,
    CAR_TYPE_CODE             VARCHAR(12)  NOT NULL,
    CAR_TYPE_DESCRIPTION_ES   VARCHAR(144) NOT NULL,
    BRANCH_OFFICE_ID          INT          NOT NULL,
    BRANCH_OFFICE_NAME        VARCHAR(96)  NOT NULL,
    BRANCH_OFFICE_CODE        VARCHAR(12)  NOT NULL,
    NIV                       VARCHAR(96)  NOT NULL,
    YEAR                      INT          NOT NULL,
    EXPEDITION                INT          NOT NULL,
    CAPACITY                  INT          NOT NULL,
    USER_ID                   INT          NOT NULL,
    CAR_MODEL                 VARCHAR(96)  NOT NULL
);


-- AUTO-GENERATED DEFINITION
CREATE TABLE DIM_PAYMENT_METHOD
(
    WALLET_ID                          INT                                    NOT NULL,
    USER_ID                            INT                                    NOT NULL,
    PAYMENT_METHOD_ID                  INT                                    NOT NULL,
    PAYMENT_METHOD_TYPE_ID             INT                                    NOT NULL,
    PAYMENT_METHOD_TYPE_CODE           VARCHAR(12)                            NOT NULL,
    PAYMENT_METHOD_TYPE_DESCRIPTION_ES VARCHAR(144)                           NOT NULL,
    CREDIT_CARD_ID                     INT                                    NOT NULL,
    CREDIT_CARD_NUMBER                 VARCHAR(16)                            NULL,
    CREDIT_CARD_EXPIRY_DATE            VARCHAR(5)                             NULL,
    PAYPAL_ACCOUNT_ID                  INT                                    NULL,
    PAYPAL_ACCOUNT_EMAIL               VARCHAR(72)                            NULL,
    PAYPAL_ACCOUNT_EMAIL_PASSWORD      VARCHAR(12) CHARSET UTF8MB4 DEFAULT '' NOT NULL
);


-- AUTO-GENERATED DEFINITION
CREATE TABLE DIM_PERSON
(
    PERSON_ID                  INT          NOT NULL,
    NAME                       VARCHAR(96)  NOT NULL,
    SECOND_NAME                VARCHAR(96)  NULL,
    LAST_NAME                  VARCHAR(96)  NOT NULL,
    SECOND_LAST_NAME           VARCHAR(96)  NULL,
    CURP                       VARCHAR(16)  NULL,
    RFC                        VARCHAR(13)  NOT NULL,
    INE_NUMBER                 VARCHAR(24)  NULL,
    PERSON_TYPE_CODE           VARCHAR(12)  NOT NULL,
    PERSON_TYPE_DESCRIPTION_ES VARCHAR(144) NOT NULL,
    USER_ID                    INT          NOT NULL
);


-- auto-generated definition
create table DIM_RENTAL
(
    TRIP_ID                               int            not null,
    TRIP_NUMBER                           varchar(16)    not null,
    USER_ID                               int            not null,
    RENTAL_DATE                           date           not null,
    DELIVERY_DATE                         date           not null,
    BRANCH_OFFICE_ID                      int            not null,
    BRANCH_CODE                           varchar(12)    not null,
    PAYMENT_METHOD_ID                     int            not null,
    LU_PAYMENT_METHOD_TYPE_CODE           varchar(12)    not null,
    LU_PAYMENT_METHOD_TYPE_DESCRIPTION_ES varchar(144)   not null,
    FARE                                  decimal(14, 8) not null,
    DAMAGE_FEE                            decimal(14, 8) not null,
    CAR_ID                                int            not null,
    NIV                                   varchar(96)    not null
);





-- AUTO-GENERATED DEFINITION
CREATE TABLE DIM_USER
(
    USER_ID                  INT                                    NOT NULL,
    PHONE                    VARCHAR(12)                            NOT NULL,
    PASSWORD                 VARCHAR(13) CHARSET UTF8MB4 DEFAULT '' NOT NULL,
    USER_TYPE_CODE           VARCHAR(12)                            NOT NULL,
    USER_TYPE_DESCRIPTION_ES VARCHAR(144)                           NOT NULL
);



-- auto-generated definition
create table AGG_RENTALS
(
    CAR_ID               int              not null,
    TOTAL_RENTS          bigint default 0 not null,
    CAR_REGISTRATION     varchar(96)      not null,
    PAYMENT_METHOD       varchar(144)     not null,
    CAR_YEAR             int              not null,
    CAR_MODEL            varchar(96)      not null,
    MOTOR_DESCRIPTION_ES varchar(144)     not null,
    RENTA_BRANCH_OFFICE  varchar(96)      not null,
    BRANCH_OFFICE_CP     varchar(8)       not null,
    BRANCH_OFFICE_STATE  varchar(96)      not null,
    AVG_DAYS             decimal(10, 4)   null,
    TOTAL_FARE           decimal(36, 8)   null,
    TOTA_DAMAGE_FEE      decimal(36, 8)   null
);




