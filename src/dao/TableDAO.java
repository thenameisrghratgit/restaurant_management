package dao;

import model.RestaurantTable;
import util.DBConnection;

import java.sql.*;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

public class TableDAO {

    // GET ALL TABLES
    public List<RestaurantTable> getAllTables() throws SQLException {

        List<RestaurantTable> tables = new ArrayList<>();

        String sql = "SELECT * FROM restaurant_tables ORDER BY table_number";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {

                RestaurantTable table = new RestaurantTable(
                        rs.getInt("table_id"),
                        rs.getInt("table_number"),
                        rs.getInt("capacity"),
                        rs.getString("status")
                );

                tables.add(table);
            }
        }

        return tables;
    }

    // GET TABLE BY ID
    public RestaurantTable getTableById(int tableId) throws SQLException {

        String sql = "SELECT * FROM restaurant_tables WHERE table_id = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, tableId);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {

                    return new RestaurantTable(
                            rs.getInt("table_id"),
                            rs.getInt("table_number"),
                            rs.getInt("capacity"),
                            rs.getString("status")
                    );
                }
            }

        }

        return null;
    }

    /**
     * Returns tables that are free for a given date/time slot and large
     * enough for the requested number of guests.
     *
     * Availability is computed per slot: a table is only excluded when a
     * non-cancelled reservation already exists for the same date and time.
     *
     * @param excludeReservationId reservation ignored during the conflict
     *                              check (used when modifying a booking);
     *                              pass -1 when creating a new reservation
     */
    public List<RestaurantTable> getAvailableTables(LocalDate date,
                                                    LocalTime time,
                                                    int minCapacity,
                                                    int excludeReservationId)
            throws SQLException {

        List<RestaurantTable> tables = new ArrayList<>();

        String sql = """
                SELECT t.* FROM restaurant_tables t
                WHERE t.capacity >= ?
                  AND NOT EXISTS (
                      SELECT 1 FROM reservations r
                      WHERE r.table_id = t.table_id
                        AND r.reservation_date = ?
                        AND r.reservation_time = ?
                        AND r.status <> 'CANCELLED'
                        AND r.reservation_id <> ?
                  )
                ORDER BY t.table_number
                """;

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, minCapacity);
            ps.setDate(2, Date.valueOf(date));
            ps.setTime(3, Time.valueOf(time));
            ps.setInt(4, excludeReservationId);

            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {

                    tables.add(new RestaurantTable(
                            rs.getInt("table_id"),
                            rs.getInt("table_number"),
                            rs.getInt("capacity"),
                            rs.getString("status")
                    ));
                }
            }
        }

        return tables;
    }

    /**
     * Dashboard metric: total number of tables in the restaurant.
     */
    public int getTotalTableCount() {
        String sql = "SELECT COUNT(*) FROM restaurant_tables";
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