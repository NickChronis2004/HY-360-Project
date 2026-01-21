const mysql = require('mysql2/promise');

let connection;

async function getConnection() {
    if (!connection) {
        connection = await mysql.createConnection({
            host: 'localhost',
            port: 3306,
            user: 'root',
            password: '',
        });
        console.log('MySQL connection established.');
    }
    return connection;
}

async function initDatabase() {
    try {
        const conn = await getConnection();

        await conn.query(`CREATE DATABASE IF NOT EXISTS HY360`);
        await conn.query(`USE HY360`);

        const createEmployeeTableQuery = `
      CREATE TABLE IF NOT EXISTS employees (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        firstname VARCHAR(50) NOT NULL,
        lastname VARCHAR(50) NOT NULL,
        marital_status VARCHAR(50) NOT NULL,
        num_children INT DEFAULT 0,
        department VARCHAR(50) NOT NULL,
        hire_date DATE NOT NULL,
        address VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        bank_account VARCHAR(40) NOT NULL,
        bank_name VARCHAR(50),
        employee_status VARCHAR(20) NOT NULL
     )
    `;

        const createContractsTableQuery = `
        CREATE TABLE IF NOT EXISTS contracts (
          contract_id INT AUTO_INCREMENT PRIMARY KEY,
          employee_id INT  NOT NULL,
          contract_start DATE NOT NULL,
          contract_end DATE NOT NULL,
          contract_salary FLOAT NOT NULL,
          employee_status VARCHAR(20) NOT NULL,
          FOREIGN KEY (employee_id) REFERENCES contract_employees(employee_id)
        )`;

        const createPaymentsTableQuery = `
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT NOT NULL,
            payment_date DATE NOT NULL,
            reference_month VARCHAR(50) NOT NULL,
            base_salary FLOAT NOT NULL,
            years_increase FLOAT DEFAULT 0,
            family_allowance FLOAT DEFAULT 0,
            research_allowance FLOAT DEFAULT 0,
            library_allowance FLOAT DEFAULT 0,
            total_amount FLOAT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )`;

        const createBaseSalariesTableQuery = `
        CREATE TABLE IF NOT EXISTS base_salaries (
            base_salary_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_type VARCHAR(50) NOT NULL,
            category VARCHAR(50) NOT NULL,
            amount FLOAT NOT NULL,
            valid_from DATE NOT NULL,
            valid_to DATE
        )`;

        const createAllowancesTableQuery = `
        CREATE TABLE IF NOT EXISTS allowances (
            allowance_id INT AUTO_INCREMENT PRIMARY KEY,
            allowance_type VARCHAR(50) NOT NULL,
            calculation_method VARCHAR(50) NOT NULL,
            price FLOAT NOT NULL,
            applied_to VARCHAR(50) NOT NULL,
            valid_from DATE NOT NULL,
            valid_to DATE
        )`;

        const createPermanentEmployeesTableQuery = `
        CREATE TABLE IF NOT EXISTS permanent_employees (
            employee_id INT PRIMARY KEY,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) 
            ON DELETE CASCADE ON UPDATE CASCADE -- if we delete the employee the permament attribute of his is deleted also.
        )`;
        
        const createContractEmployeesTableQuery = `
        CREATE TABLE IF NOT EXISTS contract_employees (
            employee_id INT PRIMARY KEY,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) 
            ON DELETE CASCADE ON UPDATE CASCADE -- if we delete the employee the contract attribute of his is deleted also.
        )`;

        const createTeachingStaffTableQuery = `
        CREATE TABLE IF NOT EXISTS teaching_staff (
            employee_id INT PRIMARY KEY,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) 
            ON DELETE CASCADE ON UPDATE CASCADE -- if we delete the employee the teaching attribute of his is deleted also.
        )`;

        const createAdministrativeStaffTableQuery =`
        CREATE TABLE IF NOT EXISTS administrative_staff (
            employee_id INT PRIMARY KEY,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id) 
            ON DELETE CASCADE ON UPDATE CASCADE -- if we delete the employee the administrative attribute of his is deleted also.
        )`;

        await conn.query(createEmployeeTableQuery);
        await conn.query(createPaymentsTableQuery);
        await conn.query(createBaseSalariesTableQuery);
        await conn.query(createPermanentEmployeesTableQuery);
        await conn.query(createAllowancesTableQuery);
        await conn.query(createContractEmployeesTableQuery);
        await conn.query(createContractsTableQuery);
        await conn.query(createTeachingStaffTableQuery);
        await conn.query(createAdministrativeStaffTableQuery);
        
        return `Database HY360 initialized or updated successfully (if it does not exist).`;
    } catch (err) {
        throw new Error('DB error: ' + err.message);
    }
}

async function dropDatabase() {
    try {
        const conn = await getConnection();
        await conn.query(`DROP DATABASE IF EXISTS HY360`);
        return `Database HY360 dropped successfully.`;
    } catch (err) {
        throw new Error('DB error: ' + err.message);
    }
}

module.exports = { initDatabase, dropDatabase };

async function closeConnection() {
    if (connection) {
        await connection.end();
        console.log('MySQL connection closed.');
    }
}

async function chooseAction() {
    const readLine = require('node:readline');
    const rl = readLine.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    rl.question("Choose your action: 1. Initialize Database 2. Drop Database \n> ", async (action) => {
        try {
            if (action === '1') {
                console.log("Initializing...");
                const msg = await initDatabase();
                console.log('SUCCESS:', msg);
            }
            else if (action === '2') {
                console.log("Dropping...");
                const msg = await dropDatabase();
                console.log('SUCCESS:', msg);
            }
            else {
                console.log('Invalid selection.');
            }
        } catch (err) {
            console.error('ERROR:', err.message);
        } finally {
            rl.close();              
            await closeConnection(); 
            process.exit(0);
        }
    });
}

chooseAction();