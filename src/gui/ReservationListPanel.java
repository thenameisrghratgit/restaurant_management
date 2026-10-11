package gui;

import model.ReservationDetail;

import javax.swing.*;
import java.awt.*;
import java.util.List;

/**
 * Reusable scrollable table that shows reservation details.
 * Used by the View, Search, Modify and Cancel screens.
 */
public class ReservationListPanel extends JPanel {

    private final ReservationTableModel model = new ReservationTableModel();
    private final JTable table = new JTable(model);

    public ReservationListPanel() {
        super(new BorderLayout());
        GUITheme.styleTable(table);
        add(new JScrollPane(table), BorderLayout.CENTER);
    }

    public void setReservations(List<ReservationDetail> reservations) {
        model.setRows(reservations);
    }

    /** Returns the selected reservation, or null when nothing is selected. */
    public ReservationDetail getSelectedReservation() {
        int viewRow = table.getSelectedRow();
        if (viewRow < 0) {
            return null;
        }
        return model.getRow(table.convertRowIndexToModel(viewRow));
    }

    public void selectById(int reservationId) {
        for (int modelRow = 0; modelRow < model.getRowCount(); modelRow++) {
            if (model.getRow(modelRow).getReservationId() == reservationId) {
                int viewRow = table.convertRowIndexToView(modelRow);
                table.getSelectionModel()
                        .setSelectionInterval(viewRow, viewRow);
                table.scrollRectToVisible(table.getCellRect(viewRow, 0, true));
                return;
            }
        }
        table.clearSelection();
    }

    public void clearSelection() {
        table.clearSelection();
    }

    public JTable getTable() {
        return table;
    }
}
