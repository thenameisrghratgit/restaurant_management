package dao;

import model.Customer;
import model.User;
import util.DBConnection;
import util.PasswordUtil;

import java.sql.*;

public class UserDAO {

    private final CustomerDAO customerDAO = new CustomerDAO();

    /**
     * Initializes the `users` table in the database if it doesn't already exist,
     * and seeds a default admin account (admin / admin123) if no admin exists.
     */
    public void initTable() {
        String createTableSql = """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(64) NOT NULL,
                    salt VARCHAR(32) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    role VARCHAR(20) NOT NULL,
                    customer_id INT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL
                )
                """;

        try (Connection conn = DBConnection.getConnection();
             Statement st = conn.createStatement()) {

            st.executeUpdate(createTableSql);

            // Check if default admin account exists
            String checkAdminSql = "SELECT COUNT(*) FROM users WHERE username = 'admin'";
            try (ResultSet rs = st.executeQuery(checkAdminSql)) {
                if (rs.next() && rs.getInt(1) == 0) {
                    String salt = PasswordUtil.generateSalt();
                    String hash = PasswordUtil.hashPassword("admin123", salt);

                    String insertAdmin = """
                            INSERT INTO users (username, password_hash, salt, full_name, role)
                            VALUES ('admin', ?, ?, 'System Administrator', 'ADMIN')
                            """;
                    try (PreparedStatement ps = conn.prepareStatement(insertAdmin)) {
                        ps.setString(1, hash);
                        ps.setString(2, salt);
                        ps.executeUpdate();
                    }
                    System.out.println("Default admin user created: admin / admin123");
                }
            }

        } catch (SQLException e) {
            System.err.println("Failed to initialize users table: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * Authenticates a user by username and password.
     * Returns User object if credentials are correct, null otherwise.
     */
    public User login(String username, String password) throws SQLException {
        if (username == null || password == null || username.trim().isEmpty()) {
            return null;
        }

        String sql = "SELECT * FROM users WHERE LOWER(username) = LOWER(?)";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, username.trim());

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    String salt = rs.getString("salt");
                    String storedHash = rs.getString("password_hash");

                    if (PasswordUtil.verifyPassword(password, salt, storedHash)) {
                        Integer custId = rs.getObject("customer_id") != null ? rs.getInt("customer_id") : null;
                        return new User(
                                rs.getInt("user_id"),
                                rs.getString("username"),
                                rs.getString("full_name"),
                                rs.getString("phone"),
                                rs.getString("email"),
                                rs.getString("role"),
                                custId
                        );
                    }
                }
            }
        }

        return null;
    }

    /**
     * Registers a new customer: creates a row in `customers` table,
     * and a linked login record in `users` table with role 'CUSTOMER'.
     */
    public User registerCustomer(String fullName, String username, String phone,
                                 String email, String password) throws SQLException {

        if (isUsernameTaken(username)) {
            throw new IllegalArgumentException("Username '" + username + "' is already taken.");
        }

        String salt = PasswordUtil.generateSalt();
        String passwordHash = PasswordUtil.hashPassword(password, salt);

        try (Connection conn = DBConnection.getConnection()) {
            boolean autoCommit = conn.getAutoCommit();
            conn.setAutoCommit(false);

            try {
                // 1. Insert customer record
                Customer customer = new Customer(fullName, phone, email);
                int customerId = customerDAO.addCustomer(customer, conn);
                if (customerId <= 0) {
                    throw new SQLException("Could not create customer record.");
                }

                // 2. Insert user record
                String userSql = """
                        INSERT INTO users (username, password_hash, salt, full_name, phone, email, role, customer_id)
                        VALUES (?, ?, ?, ?, ?, ?, 'CUSTOMER', ?)
                        """;

                int userId;
                try (PreparedStatement ps = conn.prepareStatement(userSql, Statement.RETURN_GENERATED_KEYS)) {
                    ps.setString(1, username.trim());
                    ps.setString(2, passwordHash);
                    ps.setString(3, salt);
                    ps.setString(4, fullName.trim());
                    ps.setString(5, phone != null ? phone.trim() : "");
                    ps.setString(6, email != null ? email.trim() : "");
                    ps.setInt(7, customerId);
                    ps.executeUpdate();

                    try (ResultSet rs = ps.getGeneratedKeys()) {
                        if (!rs.next()) {
                            throw new SQLException("Could not retrieve generated user ID.");
                        }
                        userId = rs.getInt(1);
                    }
                }

                conn.commit();

                return new User(
                        userId,
                        username.trim(),
                        fullName.trim(),
                        phone,
                        email,
                        User.ROLE_CUSTOMER,
                        customerId
                );

            } catch (SQLException e) {
                conn.rollback();
                throw e;
            } finally {
                conn.setAutoCommit(autoCommit);
            }
        }
    }

    /**
     * Checks if a username is already taken.
     */
    public boolean isUsernameTaken(String username) throws SQLException {
        String sql = "SELECT COUNT(*) FROM users WHERE LOWER(username) = LOWER(?)";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, username.trim());
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt(1) > 0;
                }
            }
        }
        return false;
    }

    /**
     * Total number of registered customers.
     */
    public int getTotalCustomerCount() {
        String sql = "SELECT COUNT(*) FROM customers";
        try (Connection conn = DBConnection.getConnection();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            if (rs.next()) {
                return rs.getInt(1);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }
}
