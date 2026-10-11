package gui;

import dao.ReservationDAO;
import dao.TableDAO;
import dao.UserDAO;
import model.ReservationDetail;
import model.User;
import util.DBConnection;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

/**
 * Operations dashboard for administrators: live KPIs, quick action buttons,
 * and an embedded recent reservations table.
 */
public class AdminDashboardPanel extends JPanel {

    private final JFrame parentFrame;
    private final ReservationDAO reservationDAO = new ReservationDAO();
    private final TableDAO tableDAO = new TableDAO();
    private final UserDAO userDAO = new UserDAO();

    // Metric display containers
    private final JPanel statsPanel = new JPanel(new GridLayout(1, 4, 16, 0));

    // Reservation Table
    private final ReservationListPanel listPanel = new ReservationListPanel();
    private final JComboBox<String> filterCombo =
            new JComboBox<>(new String[]{"All Reservations", "BOOKED", "COMPLETED", "CANCELLED"});
    private final JLabel tableHeaderLabel = new JLabel("Recent System Reservations");
    private final JLabel recordCountLabel = new JLabel("Loading...");

    private List<ReservationDetail> allReservations;

    public AdminDashboardPanel(JFrame parentFrame) {
        this.parentFrame = parentFrame;

        setLayout(new BorderLayout(0, 16));
        setBackground(GUITheme.getBackground());
        setBorder(new EmptyBorder(16, 24, 16, 24));

        add(buildTopSection(), BorderLayout.NORTH);
        add(buildCenterSection(), BorderLayout.CENTER);

        GUITheme.addThemeListener(this::applyTheme);
        refreshAllData();
    }

    private void applyTheme() {
        setBackground(GUITheme.getBackground());
        statsPanel.setOpaque(false);
        renderMetrics();
        tableHeaderLabel.setForeground(GUITheme.getText());
        recordCountLabel.setForeground(GUITheme.getMuted());
        repaint();
        revalidate();
    }

    private JPanel buildTopSection() {
        JPanel top = new JPanel();
        top.setLayout(new BoxLayout(top, BoxLayout.Y_AXIS));
        top.setOpaque(false);

        // Stats Row
        statsPanel.setOpaque(false);
        statsPanel.setPreferredSize(new Dimension(800, 88));
        statsPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 92));
        renderMetrics();
        top.add(statsPanel);
        top.add(Box.createVerticalStrut(14));

        // Quick Actions Row
        JPanel actions = buildQuickActionsBar();
        actions.setMaximumSize(new Dimension(Integer.MAX_VALUE, 65));
        top.add(actions);

        return top;
    }

    private void renderMetrics() {
        statsPanel.removeAll();

        int totalTables = tableDAO.getTotalTableCount();
        int activeBookings = reservationDAO.getActiveReservationCount();
        int todayBookings = reservationDAO.getTodayReservationCount();
        int totalCustomers = userDAO.getTotalCustomerCount();

        statsPanel.add(GUITheme.statCard(
                "Total Tables",
                String.valueOf(totalTables),
                "Configured dining tables",
                GUITheme.getAccent()
        ));

        statsPanel.add(GUITheme.statCard(
                "Active Bookings",
                String.valueOf(activeBookings),
                "Confirmed active status",
                GUITheme.SUCCESS
        ));

        statsPanel.add(GUITheme.statCard(
                "Today's Reservations",
                String.valueOf(todayBookings),
                "Scheduled for today",
                new Color(59, 130, 246)
        ));

        statsPanel.add(GUITheme.statCard(
                "Total Customers",
                String.valueOf(totalCustomers),
                "Registered guest accounts",
                new Color(168, 85, 247)
        ));

        statsPanel.revalidate();
        statsPanel.repaint();
    }

    private JPanel buildQuickActionsBar() {
        JPanel card = new JPanel(new BorderLayout());
        GUITheme.card(card);
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(GUITheme.getLine(), 1, true),
                new EmptyBorder(12, 16, 12, 16)
        ));

        JPanel actions = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        actions.setOpaque(false);

        JLabel label = new JLabel("Quick Actions:");
        label.setFont(new Font("Segoe UI", Font.BOLD, 13));
        label.setForeground(GUITheme.getText());
        actions.add(label);

        JButton bookBtn = GUITheme.button("+ New Booking", GUITheme.getAccent());
        bookBtn.addActionListener(e -> openDialog(new ReservationDialog(parentFrame)));
        actions.add(bookBtn);

        JButton viewBtn = GUITheme.button("View / Filter", GUITheme.getPrimary());
        viewBtn.addActionListener(e -> openDialog(new ViewReservationsDialog(parentFrame)));
        actions.add(viewBtn);

        JButton searchBtn = GUITheme.button("Search", GUITheme.getPrimaryLight());
        searchBtn.addActionListener(e -> openDialog(new SearchReservationDialog(parentFrame)));
        actions.add(searchBtn);

        JButton modifyBtn = GUITheme.button("Modify", GUITheme.getPrimaryLight());
        modifyBtn.addActionListener(e -> openDialog(new ModifyReservationDialog(parentFrame)));
        actions.add(modifyBtn);

        JButton cancelBtn = GUITheme.button("Cancel / Delete", GUITheme.DANGER);
        cancelBtn.addActionListener(e -> openDialog(new CancelReservationDialog(parentFrame)));
        actions.add(cancelBtn);

        JButton tablesBtn = GUITheme.button("Table Availability", GUITheme.getPrimaryLight());
        tablesBtn.addActionListener(e -> openDialog(new TablesDialog(parentFrame)));
        actions.add(tablesBtn);

        JButton refreshBtn = GUITheme.outlineButton("Refresh Data", GUITheme.getLine(), GUITheme.getText());
        refreshBtn.addActionListener(e -> refreshAllData());
        actions.add(refreshBtn);

        card.add(actions, BorderLayout.CENTER);
        return card;
    }

    private JPanel buildCenterSection() {
        JPanel center = new JPanel(new BorderLayout(0, 10));
        center.setOpaque(false);

        // Header above table
        JPanel headerBar = new JPanel(new BorderLayout());
        headerBar.setOpaque(false);

        tableHeaderLabel.setFont(new Font("Segoe UI", Font.BOLD, 15));
        tableHeaderLabel.setForeground(GUITheme.getText());

        JPanel filterPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 8, 0));
        filterPanel.setOpaque(false);

        JLabel filterLbl = new JLabel("Status Filter:");
        filterLbl.setFont(GUITheme.SMALL);
        filterLbl.setForeground(GUITheme.getMuted());
        filterPanel.add(filterLbl);

        GUITheme.styleCombo(filterCombo);
        filterCombo.addActionListener(e -> applyStatusFilter());
        filterPanel.add(filterCombo);

        recordCountLabel.setFont(GUITheme.SMALL);
        recordCountLabel.setForeground(GUITheme.getMuted());
        filterPanel.add(Box.createHorizontalStrut(8));
        filterPanel.add(recordCountLabel);

        headerBar.add(tableHeaderLabel, BorderLayout.WEST);
        headerBar.add(filterPanel, BorderLayout.EAST);

        center.add(headerBar, BorderLayout.NORTH);
        center.add(listPanel, BorderLayout.CENTER);

        return center;
    }

    private void openDialog(JDialog dialog) {
        dialog.setVisible(true);
        refreshAllData();
    }

    public void refreshAllData() {
        renderMetrics();
        try {
            allReservations = reservationDAO.getAllReservationDetails();
            applyStatusFilter();
        } catch (SQLException e) {
            e.printStackTrace();
            recordCountLabel.setText("Failed to load reservations.");
        }
    }

    private void applyStatusFilter() {
        if (allReservations == null) {
            return;
        }

        String filter = (String) filterCombo.getSelectedItem();
        List<ReservationDetail> filtered = allReservations;

        if (filter != null && !"All Reservations".equalsIgnoreCase(filter)) {
            filtered = allReservations.stream()
                    .filter(r -> filter.equalsIgnoreCase(r.getStatus()))
                    .toList();
        }

        listPanel.setReservations(filtered);
        recordCountLabel.setText("Showing " + filtered.size() + " of " + allReservations.size() + " records");
    }
}
