package gui;

import dao.ReservationDAO;
import model.Reservation;
import model.ReservationDetail;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.SQLException;
import java.util.List;

/**
 * Cancel screen.
 *
 * Two ways to remove a booking from the active schedule:
 * - CANCEL  -> UPDATE statement, keeps the row as booking history
 * - DELETE  -> DELETE statement (requires confirmation, removes the row)
 */
public class CancelReservationDialog extends JDialog {

    private final ReservationListPanel listPanel = new ReservationListPanel();
    private final JLabel selectedLabel =
            GUITheme.label("Select a reservation in the list above.");
    private final JButton cancelButton = GUITheme.button(
            "Cancel Reservation (Set Status = CANCELLED)", GUITheme.PRIMARY_LIGHT);
    private final JButton deleteButton = GUITheme.button(
            "Delete Permanently", GUITheme.DANGER);

    private final ReservationDAO reservationDAO = new ReservationDAO();

    public CancelReservationDialog(JFrame owner) {
        super(owner, "Cancel Reservation", true);
        setSize(940, 600);
        setLocationRelativeTo(owner);
        setMinimumSize(new Dimension(760, 460));
        setLayout(new BorderLayout());

        add(GUITheme.dialogHeader("Cancel / Delete Reservation",
                "Cancel keeps the booking history, delete removes the record"),
                BorderLayout.NORTH);
        add(buildCenter(), BorderLayout.CENTER);
        add(buildButtonBar(), BorderLayout.SOUTH);

        attachListeners();
        loadReservations();
    }

    private JPanel buildCenter() {
        JPanel center = new JPanel(new BorderLayout(0, 8));
        center.setBackground(GUITheme.BACKGROUND);
        center.setBorder(new EmptyBorder(12, 16, 8, 16));

        JPanel toolbar = new JPanel(new BorderLayout());
        toolbar.setOpaque(false);

        JButton refresh = GUITheme.button("Refresh List",
                GUITheme.PRIMARY_LIGHT);
        refresh.addActionListener(e -> loadReservations());
        toolbar.add(refresh, BorderLayout.WEST);

        selectedLabel.setFont(GUITheme.SMALL);
        toolbar.add(selectedLabel, BorderLayout.EAST);

        center.add(toolbar, BorderLayout.NORTH);
        center.add(listPanel, BorderLayout.CENTER);
        return center;
    }

    private JPanel buildButtonBar() {
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 12));
        bar.setBackground(GUITheme.BACKGROUND);

        JButton close = GUITheme.button("Close", GUITheme.PRIMARY);
        close.addActionListener(e -> dispose());

        cancelButton.addActionListener(e -> cancelReservation());
        deleteButton.addActionListener(e -> deleteReservation());
        cancelButton.setEnabled(false);
        deleteButton.setEnabled(false);

        bar.add(cancelButton);
        bar.add(deleteButton);
        bar.add(close);
        return bar;
    }

    private void attachListeners() {
        listPanel.getTable().getSelectionModel()
                .addListSelectionListener(e -> {
                    if (e.getValueIsAdjusting()) {
                        return;
                    }
                    ReservationDetail selected =
                            listPanel.getSelectedReservation();
                    boolean hasSelection = selected != null;

                    cancelButton.setEnabled(hasSelection);
                    deleteButton.setEnabled(hasSelection);

                    if (hasSelection) {
                        selectedLabel.setText("Selected: #"
                                + selected.getReservationId() + " - "
                                + selected.getCustomerName() + " ("
                                + selected.getStatus() + ")");
                    } else {
                        selectedLabel.setText(
                                "Select a reservation in the list above.");
                    }
                });
    }

    private void loadReservations() {
        try {
            List<ReservationDetail> all =
                    reservationDAO.getAllReservationDetails();
            listPanel.setReservations(all);
            updateButtonStates();
        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Could not load reservations:\n" + e.getMessage());
        }
    }

    private void updateButtonStates() {
        ReservationDetail selected = listPanel.getSelectedReservation();
        cancelButton.setEnabled(selected != null);
        deleteButton.setEnabled(selected != null);
    }

    // ================================================================
    //  UPDATE - cancel without losing history
    // ================================================================

    private void cancelReservation() {
        ReservationDetail selected = listPanel.getSelectedReservation();
        if (selected == null) {
            GUITheme.error(this, "Select a reservation to cancel.");
            return;
        }

        if ("CANCELLED".equals(selected.getStatus())) {
            GUITheme.info(this,
                    "Reservation #" + selected.getReservationId()
                            + " is already cancelled.");
            return;
        }

        boolean yes = GUITheme.confirm(this,
                "Cancel reservation #" + selected.getReservationId()
                        + " for " + selected.getCustomerName() + "?\n\n"
                        + "The record is kept with status CANCELLED.",
                "Confirm Cancellation");
        if (!yes) {
            return;
        }

        try {
            // READ first, then UPDATE the status
            Reservation reservation =
                    reservationDAO.getReservationById(
                            selected.getReservationId());

            if (reservation == null) {
                GUITheme.error(this,
                        "Reservation not found - it may already be deleted.");
                loadReservations();
                return;
            }

            reservation.setStatus("CANCELLED");
            boolean updated = reservationDAO.updateReservation(reservation);

            if (updated) {
                GUITheme.success(this,
                        "Reservation #" + reservation.getReservationId()
                                + " has been cancelled.\n"
                                + "Table "
                                + selected.getTableNumber()
                                + " is free again for that slot.");
            } else {
                GUITheme.error(this,
                        "The reservation could not be cancelled.");
            }

            loadReservations();

        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Database error while cancelling:\n" + e.getMessage());
        }
    }

    // ================================================================
    //  DELETE - removes the row permanently
    // ================================================================

    private void deleteReservation() {
        ReservationDetail selected = listPanel.getSelectedReservation();
        if (selected == null) {
            GUITheme.error(this, "Select a reservation to delete.");
            return;
        }

        boolean yes = GUITheme.confirm(this,
                "PERMANENTLY delete reservation #" + selected.getReservationId()
                        + " for " + selected.getCustomerName() + "?\n\n"
                        + "This removes the record from the database and "
                        + "cannot be undone.\n"
                        + "(Use 'Cancel' instead if you only want to "
                        + "stop the booking.)",
                "Confirm Permanent Deletion");
        if (!yes) {
            return;
        }

        try {
            boolean deleted =
                    reservationDAO.deleteReservation(
                            selected.getReservationId());

            if (deleted) {
                GUITheme.success(this,
                        "Reservation #" + selected.getReservationId()
                                + " was deleted from the database.");
            } else {
                GUITheme.error(this,
                        "The reservation could not be deleted "
                                + "(it may already be gone).");
            }

            loadReservations();

        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Database error while deleting:\n" + e.getMessage());
        }
    }
}
