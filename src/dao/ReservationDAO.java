package dao;

import model.Customer;
import model.Reservation;
import model.ReservationDetail;
import util.DBConnection;

import java.sql.*;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class ReservationDAO {

    // ----- search criteria codes used by searchReservationDetails() -----
    public static final String SEARCH_ID = "ID";
    public static final String SEARCH_NAME = "NAME";
    public static final String SEARCH_PHONE = "PHONE";

    // Shared SELECT for every JOIN query so results stay consistent
    private static final String DETAIL_SELECT = """
            SELECT r.reservation_id, r.customer_id, r.table_id,
                   r.reservation_date, r.reservation_time, r.guests, r.status,
                   c.name AS customer_name, c.phone AS customer_phone,
                   t.table_number AS table_number
            FROM reservations r
            JOIN customers c ON c.customer_id = r.customer_id
            JOIN restaurant_tables t ON t.table_id = r.table_id""";

    // ================================================================
    //  CREATE
    // ================================================================

    // CREATE / INSERT
    public boolean addReservation(Reservation reservation)
            throws SQLException {

        String sql = """
                INSERT INTO reservations
                (customer_id, table_id, reservation_date,
                 reservation_time, guests, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """;

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, reservation.getCustomerId());
            ps.setInt(2, reservation.getTableId());
            ps.setDate(3,
                    Date.valueOf(reservation.getReservationDate()));
            ps.setTime(4,
                    Time.valueOf(reservation.getReservationTime()));
            ps.setInt(5, reservation.getGuests());
            ps.setString(6, reservation.getStatus());

            return ps.executeUpdate() > 0;
        }
    }

    /**
     * Books a reservation atomically: the customer row and the reservation
     * row are inserted inside one database transaction, so either both are
     * saved or neither is.
     *
     * @return the generated reservation_id
     */
    public int bookReservation(Customer customer, Reservation reservation)
            throws SQLException {

        String insertCustomer =
                "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)";

        String insertReservation = """
                INSERT INTO reservations
                (customer_id, table_id, reservation_date,
                 reservation_time, guests, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """;

        try (Connection conn = DBConnection.getConnection()) {

            boolean autoCommit = conn.getAutoCommit();
            conn.setAutoCommit(false);

            try {
                int customerId;

                try (PreparedStatement ps = conn.prepareStatement(
                        insertCustomer, Statement.RETURN_GENERATED_KEYS)) {

                    ps.setString(1, customer.getName());
                    ps.setString(2, customer.getPhone());
                    ps.setString(3, customer.getEmail());
                    ps.executeUpdate();

                    try (ResultSet rs = ps.getGeneratedKeys()) {
                        if (!rs.next()) {
                            throw new SQLException(
                                    "Customer insert did not return an ID.");
                        }
                        customerId = rs.getInt(1);
                    }
                }

                int reservationId;

                try (PreparedStatement ps = conn.prepareStatement(
                        insertReservation, Statement.RETURN_GENERATED_KEYS)) {

                    ps.setInt(1, customerId);
                    ps.setInt(2, reservation.getTableId());
                    ps.setDate(3,
                            Date.valueOf(reservation.getReservationDate()));
                    ps.setTime(4,
                            Time.valueOf(reservation.getReservationTime()));
                    ps.setInt(5, reservation.getGuests());
                    ps.setString(6, reservation.getStatus());
                    ps.executeUpdate();

                    try (ResultSet rs = ps.getGeneratedKeys()) {
                        if (!rs.next()) {
                            throw new SQLException(
                                    "Reservation insert did not return an ID.");
                        }
                        reservationId = rs.getInt(1);
                    }
                }

                conn.commit();

                reservation.setCustomerId(customerId);
                reservation.setReservationId(reservationId);

                return reservationId;

            } catch (SQLException e) {
                conn.rollback();          // undo the partial booking
                throw e;
            } finally {
                conn.setAutoCommit(autoCommit);
            }
        }
    }

    // ================================================================
    //  READ
    // ================================================================

    // READ / GET ALL
    public List<Reservation> getAllReservations()
            throws SQLException {

        List<Reservation> reservations = new ArrayList<>();

        String sql = """
                SELECT * FROM reservations
                ORDER BY reservation_date, reservation_time
                """;

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {

                Reservation reservation = new Reservation(
                        rs.getInt("reservation_id"),
                        rs.getInt("customer_id"),
                        rs.getInt("table_id"),
                        rs.getDate("reservation_date").toLocalDate(),
                        rs.getTime("reservation_time").toLocalTime(),
                        rs.getInt("guests"),
                        rs.getString("status")
                );

                reservations.add(reservation);
            }
        }

        return reservations;
    }

    // READ / SEARCH BY ID
    public Reservation getReservationById(int reservationId)
            throws SQLException {

        String sql =
                "SELECT * FROM reservations WHERE reservation_id = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, reservationId);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {

                    return new Reservation(
                            rs.getInt("reservation_id"),
                            rs.getInt("customer_id"),
                            rs.getInt("table_id"),
                            rs.getDate("reservation_date").toLocalDate(),
                            rs.getTime("reservation_time").toLocalTime(),
                            rs.getInt("guests"),
                            rs.getString("status")
                    );
                }
            }
        }

        return null;
    }

    // READ / JOIN of reservations + customers + tables (for the GUI)
    public List<ReservationDetail> getAllReservationDetails()
            throws SQLException {

        String sql = DETAIL_SELECT
                + " ORDER BY r.reservation_date DESC, r.reservation_time DESC";

        List<ReservationDetail> details = new ArrayList<>();

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                details.add(mapDetail(rs));
            }
        }

        return details;
    }

    // READ / single JOIN row
    public ReservationDetail getReservationDetailById(int reservationId)
            throws SQLException {

        String sql = DETAIL_SELECT + " WHERE r.reservation_id = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, reservationId);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return mapDetail(rs);
                }
            }
        }

        return null;
    }

    /**
     * SEARCH reservations by reservation ID, customer name or phone number.
     * The search value is always bound with PreparedStatement - never
     * concatenated into the SQL string.
     */
    public List<ReservationDetail> searchReservationDetails(
            String searchBy, String text) throws SQLException {

        String where;

        switch (searchBy) {
            case SEARCH_ID -> where = " WHERE r.reservation_id = ?";
            case SEARCH_NAME -> where = " WHERE c.name LIKE ?";
            case SEARCH_PHONE -> where = " WHERE c.phone LIKE ?";
            default -> throw new IllegalArgumentException(
                    "Unknown search field: " + searchBy);
        }

        String sql = DETAIL_SELECT + where
                + " ORDER BY r.reservation_date DESC, r.reservation_time DESC";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            if (SEARCH_ID.equals(searchBy)) {
                ps.setInt(1, Integer.parseInt(text.trim()));
            } else {
                ps.setString(1, "%" + text.trim() + "%");
            }

            List<ReservationDetail> details = new ArrayList<>();

            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    details.add(mapDetail(rs));
                }
            }

            return details;
        }
    }

    /**
     * READ / Customer-specific reservations for Customer Dashboard.
     */
    public List<ReservationDetail> getReservationsByCustomerId(int customerId)
            throws SQLException {
        String sql = DETAIL_SELECT + " WHERE r.customer_id = ?"
                + " ORDER BY r.reservation_date DESC, r.reservation_time DESC";

        List<ReservationDetail> details = new ArrayList<>();
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, customerId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    details.add(mapDetail(rs));
                }
            }
        }
        return details;
    }

    /**
     * Helper to find reservations by customer phone number.
     */
    public List<ReservationDetail> getReservationsByPhone(String phone)
            throws SQLException {
        if (phone == null || phone.trim().isEmpty()) {
            return new ArrayList<>();
        }
        return searchReservationDetails(SEARCH_PHONE, phone.trim());
    }

    /**
     * Dashboard metric: count of active bookings (status = 'BOOKED').
     */
    public int getActiveReservationCount() {
        String sql = "SELECT COUNT(*) FROM reservations WHERE status = 'BOOKED'";
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

    /**
     * Dashboard metric: count of reservations for today.
     */
    public int getTodayReservationCount() {
        String sql = "SELECT COUNT(*) FROM reservations WHERE reservation_date = CURDATE() AND status <> 'CANCELLED'";
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

    // ================================================================
    //  SLOT AVAILABILITY
    // ================================================================

    /**
     * Checks whether a table is free for an exact date/time slot.
     * Cancelled reservations do not block a table.
     */
    public boolean isTableSlotFree(int tableId, LocalDate date,
                                   LocalTime time, int excludeReservationId)
            throws SQLException {

        String sql = """
                SELECT COUNT(*) FROM reservations
                WHERE table_id = ?
                  AND reservation_date = ?
                  AND reservation_time = ?
                  AND status <> 'CANCELLED'
                  AND reservation_id <> ?
                """;

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, tableId);
            ps.setDate(2, Date.valueOf(date));
            ps.setTime(3, Time.valueOf(time));
            ps.setInt(4, excludeReservationId);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt(1) == 0;
                }
            }
        }

        return true;
    }

    /**
     * Returns the IDs of all tables already booked for a date/time slot.
     * Used by the "Available Tables" screen.
     */
    public Set<Integer> getBookedTableIds(LocalDate date, LocalTime time)
            throws SQLException {

        String sql = """
                SELECT DISTINCT table_id FROM reservations
                WHERE reservation_date = ?
                  AND reservation_time = ?
                  AND status <> 'CANCELLED'
                """;

        Set<Integer> booked = new HashSet<>();

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setDate(1, Date.valueOf(date));
            ps.setTime(2, Time.valueOf(time));

            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    booked.add(rs.getInt("table_id"));
                }
            }
        }

        return booked;
    }

    // ================================================================
    //  UPDATE
    // ================================================================

    // UPDATE
    public boolean updateReservation(Reservation reservation)
            throws SQLException {

        String sql = """
                UPDATE reservations
                SET table_id = ?,
                    reservation_date = ?,
                    reservation_time = ?,
                    guests = ?,
                    status = ?
                WHERE reservation_id = ?
                """;

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, reservation.getTableId());
            ps.setDate(2,
                    Date.valueOf(reservation.getReservationDate()));
            ps.setTime(3,
                    Time.valueOf(reservation.getReservationTime()));
            ps.setInt(4, reservation.getGuests());
            ps.setString(5, reservation.getStatus());
            ps.setInt(6, reservation.getReservationId());

            return ps.executeUpdate() > 0;
        }
    }

    // ================================================================
    //  DELETE
    // ================================================================

    // DELETE / CANCEL
    public boolean deleteReservation(int reservationId)
            throws SQLException {

        String sql =
                "DELETE FROM reservations WHERE reservation_id = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, reservationId);

            return ps.executeUpdate() > 0;
        }
    }

    // ----- helper: map one JOIN result row to a ReservationDetail -----
    private static ReservationDetail mapDetail(ResultSet rs)
            throws SQLException {

        return new ReservationDetail(
                rs.getInt("reservation_id"),
                rs.getInt("customer_id"),
                rs.getInt("table_id"),
                rs.getInt("table_number"),
                rs.getString("customer_name"),
                rs.getString("customer_phone"),
                rs.getDate("reservation_date").toLocalDate(),
                rs.getTime("reservation_time").toLocalTime(),
                rs.getInt("guests"),
                rs.getString("status")
        );
    }
}
