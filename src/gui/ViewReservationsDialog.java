package gui;

import dao.ReservationDAO;
import model.ReservationDetail;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.SQLException;
import java.util.List;

/**
 * Read-only screen that lists every reservation in a JTable.
 */
public class ViewReservationsDialog extends JDialog {

    private static final String FILTER_ALL = "All Reservations";

    private final ReservationListPanel listPanel = new ReservationListPanel();
    private final JComboBox<String> filterCombo =
            new JComboBox<>(new String[]{
                    FILTER_ALL, "BOOKED", "COMPLETED", "CANCELLED"});
    private final JLabel countLabel = new JLabel();

    private final ReservationDAO reservationDAO = new ReservationDAO();
    private List<ReservationDetail> allReservations;

    public ViewReservationsDialog(JFrame owner) {
        super(owner, "View Reservations", true);
        setSize(940, 560);
        setLocationRelativeTo(owner);
        setMinimumSize(new Dimension(760, 420));
        setLayout(new BorderLayout());

        add(GUITheme.dialogHeader("All Reservations",
                "Live data from the reservations table (JOIN with customers and tables)"),
                BorderLayout.NORTH);
        add(buildToolbar(), BorderLayout.CENTER);
        add(buildButtonBar(), BorderLayout.SOUTH);

        filterCombo.addActionListener(e -> applyFilter());
        loadReservations();
    }

    private JPanel buildToolbar() {
        JPanel toolbar = new JPanel(new BorderLayout(12, 0));
        toolbar.setBackground(GUITheme.BACKGROUND);
        toolbar.setBorder(new EmptyBorder(14, 16, 10, 16));

        JPanel filterPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 0));
        filterPanel.setOpaque(false);
        filterPanel.add(GUITheme.label("Show:"));
        GUITheme.styleCombo(filterCombo);
        filterPanel.add(filterCombo);

        JButton refreshButton = GUITheme.button("Refresh",
                GUITheme.PRIMARY_LIGHT);
        refreshButton.addActionListener(e -> loadReservations());
        filterPanel.add(refreshButton);

        toolbar.add(filterPanel, BorderLayout.WEST);

        countLabel.setFont(GUITheme.SMALL);
        countLabel.setForeground(GUITheme.MUTED);
        toolbar.add(countLabel, BorderLayout.EAST);

        JPanel center = new JPanel(new BorderLayout());
        center.setBackground(GUITheme.BACKGROUND);
        center.setBorder(new EmptyBorder(0, 16, 0, 16));
        center.add(toolbar, BorderLayout.NORTH);
        center.add(listPanel, BorderLayout.CENTER);
        return center;
    }

    private JPanel buildButtonBar() {
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 12));
        bar.setBackground(GUITheme.BACKGROUND);

        JButton close = GUITheme.button("Close", GUITheme.PRIMARY);
        close.addActionListener(e -> dispose());
        bar.add(close);
        return bar;
    }

    private void loadReservations() {
        try {
            allReservations = reservationDAO.getAllReservationDetails();
            applyFilter();
        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Could not load reservations:\n" + e.getMessage());
        }
    }

    /** In-memory status filter applied on top of the loaded list. */
    private void applyFilter() {
        if (allReservations == null) {
            return;
        }

        String selected = (String) filterCombo.getSelectedItem();
        List<ReservationDetail> filtered = allReservations;

        if (!FILTER_ALL.equals(selected)) {
            filtered = allReservations.stream()
                    .filter(d -> selected.equalsIgnoreCase(d.getStatus()))
                    .toList();
        }

        listPanel.setReservations(filtered);
        countLabel.setText(filtered.size() + " of "
                + allReservations.size() + " reservation(s)");
    }
}
