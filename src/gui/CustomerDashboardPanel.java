package gui;

import dao.CustomerDAO;
import dao.ReservationDAO;
import dao.TableDAO;
import model.Customer;
import model.Reservation;
import model.ReservationDetail;
import model.User;
import util.UserSession;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.SQLException;
import java.util.List;

/**
 * Clean and intuitive portal for dining customers:
 * view personal bookings, book new tables, check slot availability,
 * and cancel active reservations.
 */
public class CustomerDashboardPanel extends JPanel {

    private final JFrame parentFrame;
    private final ReservationDAO reservationDAO = new ReservationDAO();
    private final CustomerDAO customerDAO = new CustomerDAO();
    private final TableDAO tableDAO = new TableDAO();

    private Customer customer;

    // Stats
    private final JPanel statsPanel = new JPanel(new GridLayout(1, 3, 16, 0));

    // Reservation Table
    private final ReservationListPanel listPanel = new ReservationListPanel();
    private final JLabel greetingLabel = new JLabel("Welcome!");
    private final JLabel countLabel = new JLabel("Loading your reservations...");

    private List<ReservationDetail> customerReservations;

    public CustomerDashboardPanel(JFrame parentFrame) {
        this.parentFrame = parentFrame;

        setLayout(new BorderLayout(0, 16));
        setBackground(GUITheme.getBackground());
        setBorder(new EmptyBorder(16, 24, 16, 24));

        add(buildTopSection(), BorderLayout.NORTH);
        add(buildCenterSection(), BorderLayout.CENTER);

        GUITheme.addThemeListener(this::applyTheme);
    }

    public void initCustomerData() {
        User user = UserSession.getCurrentUser();
        if (user != null) {
            greetingLabel.setText("Welcome, " + user.getFullName() + "!");
            if (user.getCustomerId() != null) {
                try {
                    customer = customerDAO.getCustomerById(user.getCustomerId());
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
            if (customer == null) {
                customer = new Customer(user.getFullName(), user.getPhone(), user.getEmail());
            }
        }
        refreshData();
    }

    private void applyTheme() {
        setBackground(GUITheme.getBackground());
        statsPanel.setOpaque(false);
        greetingLabel.setForeground(GUITheme.getText());
        countLabel.setForeground(GUITheme.getMuted());
        renderMetrics();
        repaint();
        revalidate();
    }

    private JPanel buildTopSection() {
        JPanel top = new JPanel();
        top.setLayout(new BoxLayout(top, BoxLayout.Y_AXIS));
        top.setOpaque(false);

        // Header greeting
        JPanel greetBox = new JPanel(new BorderLayout(0, 4));
        greetBox.setOpaque(false);
        greetBox.setMaximumSize(new Dimension(Integer.MAX_VALUE, 50));

        greetingLabel.setFont(new Font("Segoe UI", Font.BOLD, 22));
        greetingLabel.setForeground(GUITheme.getText());

        JLabel subLabel = new JLabel("Manage your dining reservations and check available tables");
        subLabel.setFont(GUITheme.SMALL);
        subLabel.setForeground(GUITheme.getMuted());

        greetBox.add(greetingLabel, BorderLayout.NORTH);
        greetBox.add(subLabel, BorderLayout.SOUTH);

        top.add(greetBox);
        top.add(Box.createVerticalStrut(10));

        // Stats Cards Row
        statsPanel.setOpaque(false);
        statsPanel.setPreferredSize(new Dimension(800, 88));
        statsPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 92));
        renderMetrics();
        top.add(statsPanel);
        top.add(Box.createVerticalStrut(14));

        // Action Buttons Row
        JPanel actions = buildActionsBar();
        actions.setMaximumSize(new Dimension(Integer.MAX_VALUE, 65));
        top.add(actions);

        return top;
    }

    private void renderMetrics() {
        statsPanel.removeAll();

        int total = customerReservations != null ? customerReservations.size() : 0;
        int active = 0;
        if (customerReservations != null) {
            for (ReservationDetail r : customerReservations) {
                if ("BOOKED".equalsIgnoreCase(r.getStatus())) {
                    active++;
                }
            }
        }

        User user = UserSession.getCurrentUser();
        String phoneStr = (user != null && user.getPhone() != null && !user.getPhone().isEmpty())
                ? user.getPhone()
                : "Not Provided";

        statsPanel.add(GUITheme.statCard(
                "My Active Bookings",
                String.valueOf(active),
                "Confirmed upcoming tables",
                GUITheme.SUCCESS
        ));

        statsPanel.add(GUITheme.statCard(
                "Total Reservations",
                String.valueOf(total),
                "Lifetime reservations",
                GUITheme.getAccent()
        ));

        statsPanel.add(GUITheme.statCard(
                "Registered Contact",
                phoneStr,
                "Linked phone number",
                new Color(59, 130, 246)
        ));

        statsPanel.revalidate();
        statsPanel.repaint();
    }

    private JPanel buildActionsBar() {
        JPanel card = new JPanel(new BorderLayout());
        GUITheme.card(card);
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(GUITheme.getLine(), 1, true),
                new EmptyBorder(12, 16, 12, 16)
        ));

        JPanel actions = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        actions.setOpaque(false);

        JButton bookBtn = GUITheme.button("+ Reserve a Table", GUITheme.getAccent());
        bookBtn.addActionListener(e -> bookTable());
        actions.add(bookBtn);

        JButton tablesBtn = GUITheme.button("Check Available Tables", GUITheme.getPrimaryLight());
        tablesBtn.addActionListener(e -> {
            TablesDialog dialog = new TablesDialog(parentFrame);
            dialog.setVisible(true);
        });
        actions.add(tablesBtn);

        JButton cancelBtn = GUITheme.button("Cancel Selected Booking", GUITheme.DANGER);
        cancelBtn.addActionListener(e -> cancelSelectedBooking());
        actions.add(cancelBtn);

        JButton refreshBtn = GUITheme.outlineButton("Refresh Bookings", GUITheme.getLine(), GUITheme.getText());
        refreshBtn.addActionListener(e -> refreshData());
        actions.add(refreshBtn);

        card.add(actions, BorderLayout.CENTER);
        return card;
    }

    private JPanel buildCenterSection() {
        JPanel center = new JPanel(new BorderLayout(0, 10));
        center.setOpaque(false);

        JPanel headerBar = new JPanel(new BorderLayout());
        headerBar.setOpaque(false);

        JLabel tblTitle = new JLabel("My Booking History");
        tblTitle.setFont(new Font("Segoe UI", Font.BOLD, 15));
        tblTitle.setForeground(GUITheme.getText());

        countLabel.setFont(GUITheme.SMALL);
        countLabel.setForeground(GUITheme.getMuted());

        headerBar.add(tblTitle, BorderLayout.WEST);
        headerBar.add(countLabel, BorderLayout.EAST);

        center.add(headerBar, BorderLayout.NORTH);
        center.add(listPanel, BorderLayout.CENTER);

        return center;
    }

    private void bookTable() {
        ReservationDialog dialog = new ReservationDialog(parentFrame, customer);
        dialog.setVisible(true);
        refreshData();
    }

    private void cancelSelectedBooking() {
        ReservationDetail selected = listPanel.getSelectedReservation();
        if (selected == null) {
            GUITheme.info(this, "Please select one of your reservations in the table above to cancel.");
            return;
        }

        if ("CANCELLED".equalsIgnoreCase(selected.getStatus())) {
            GUITheme.info(this, "Reservation #" + selected.getReservationId() + " is already cancelled.");
            return;
        }

        boolean confirm = GUITheme.confirm(this,
                "Are you sure you want to cancel Reservation #" + selected.getReservationId()
                        + " for Table " + selected.getTableNumber() + " on " + selected.getDateText() + "?\n"
                        + "This will release the table slot for other guests.",
                "Confirm Cancellation");

        if (confirm) {
            try {
                // Update reservation status to CANCELLED
                Reservation res = reservationDAO.getReservationById(selected.getReservationId());
                if (res != null) {
                    res.setStatus("CANCELLED");
                    boolean ok = reservationDAO.updateReservation(res);
                    if (ok) {
                        GUITheme.success(this, "Reservation #" + selected.getReservationId() + " has been cancelled.");
                        refreshData();
                    } else {
                        GUITheme.error(this, "Could not cancel reservation.");
                    }
                }
            } catch (SQLException e) {
                e.printStackTrace();
                GUITheme.error(this, "Error cancelling reservation:\n" + e.getMessage());
            }
        }
    }

    public void refreshData() {
        User user = UserSession.getCurrentUser();
        if (user == null) {
            return;
        }

        try {
            if (user.getCustomerId() != null) {
                customerReservations = reservationDAO.getReservationsByCustomerId(user.getCustomerId());
            } else if (user.getPhone() != null && !user.getPhone().isEmpty()) {
                customerReservations = reservationDAO.getReservationsByPhone(user.getPhone());
            } else {
                customerReservations = reservationDAO.searchReservationDetails(
                        ReservationDAO.SEARCH_NAME, user.getFullName());
            }

            listPanel.setReservations(customerReservations);
            countLabel.setText(customerReservations.size() + " reservation(s) on file");
            renderMetrics();

        } catch (SQLException e) {
            e.printStackTrace();
            countLabel.setText("Error loading reservations: " + e.getMessage());
        }
    }
}
