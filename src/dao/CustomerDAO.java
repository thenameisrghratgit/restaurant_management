package dao;

import model.Customer;
import util.DBConnection;

import java.sql.*;

public class CustomerDAO {

    // INSERT customer (opens its own connection)
    public int addCustomer(Customer customer) throws SQLException {

        try (Connection conn = DBConnection.getConnection()) {
            return addCustomer(customer, conn);
        }
    }

    /**
     * INSERT customer using an existing connection so that it can take part
     * in a larger transaction (customer + reservation booked together).
     */
    public int addCustomer(Customer customer, Connection conn)
            throws SQLException {

        String sql = "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)";

        try (PreparedStatement ps = conn.prepareStatement(
                sql, Statement.RETURN_GENERATED_KEYS)) {

            ps.setString(1, customer.getName());
            ps.setString(2, customer.getPhone());
            ps.setString(3, customer.getEmail());

            ps.executeUpdate();

            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) {
                    return rs.getInt(1);
                }
            }
        }

        return -1;
    }

    // SEARCH customer by ID
    public Customer getCustomerById(int customerId) throws SQLException {

        String sql = "SELECT * FROM customers WHERE customer_id = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, customerId);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {

                    return new Customer(
                            rs.getInt("customer_id"),
                            rs.getString("name"),
                            rs.getString("phone"),
                            rs.getString("email")
                    );
                }
            }
        }

        return null;
    }
}