import os
from PIL import Image, ImageDraw, ImageFont

def draw_diagram():
    # 2x supersampling for clean antialiasing
    scale = 2
    w, h = 1050 * scale, 800 * scale
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_bold_path = "C:/Windows/Fonts/segoeuib.ttf"
    font_reg_path = "C:/Windows/Fonts/segoeui.ttf"

    f_main_title = ImageFont.truetype(font_bold_path, 17 * scale)
    f_box_title = ImageFont.truetype(font_bold_path, 12.5 * scale)
    f_box_body = ImageFont.truetype(font_reg_path, 10 * scale)
    f_arrow_lbl = ImageFont.truetype(font_reg_path, 8.5 * scale)
    f_user_title = ImageFont.truetype(font_bold_path, 11.5 * scale)

    # Palette
    c_text_dark = (30, 41, 59, 255)
    c_text_muted = (71, 85, 105, 255)
    c_arrow = (71, 85, 105, 255)

    def draw_card(box, bg_color, border_color, title, subtitle_lines, title_color=(30, 41, 59, 255)):
        x0, y0, x1, y1 = [int(v * scale) for v in box]
        r = 8 * scale

        # Subtle shadow
        s_off = 2 * scale
        draw.rounded_rectangle(
            [x0 + s_off, y0 + s_off, x1 + s_off, y1 + s_off],
            radius=r,
            fill=(241, 245, 249, 180)
        )

        # Card body
        draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=bg_color, outline=border_color, width=max(1, int(1.5 * scale)))

        # Card Title
        draw.text((x0 + 16 * scale, y0 + 12 * scale), title, font=f_box_title, fill=title_color)

        # Subtitle lines with generous leading
        curr_y = y0 + 34 * scale
        for line in subtitle_lines:
            draw.text((x0 + 16 * scale, curr_y), line, font=f_box_body, fill=c_text_dark)
            curr_y += 16 * scale

    def draw_user_pill(cx, cy, label):
        cx_s = int(cx * scale)
        cy_s = int(cy * scale)
        pw = int(170 * scale)
        ph = int(36 * scale)
        x0 = cx_s - pw // 2
        y0 = cy_s - ph // 2
        x1 = x0 + pw
        y1 = y0 + ph
        draw.rounded_rectangle([x0, y0, x1, y1], radius=18 * scale, fill=(248, 250, 252, 255), outline=(148, 163, 184, 255), width=max(1, int(1.5 * scale)))
        
        bbox = draw.textbbox((0, 0), label, font=f_user_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx_s - tw // 2, cy_s - th // 2 - 2 * scale), label, font=f_user_title, fill=c_text_dark)
        return (cx_s, y1)

    def draw_down_arrow(x, y0, y1, label=None, label_side="right"):
        xs = int(x * scale)
        y0s = int(y0 * scale)
        y1s = int(y1 * scale)
        draw.line([(xs, y0s), (xs, y1s)], fill=c_arrow, width=max(1, int(1.5 * scale)))
        ah = 7 * scale
        aw = 5 * scale
        draw.polygon([(xs, y1s), (xs - aw, y1s - ah), (xs + aw, y1s - ah)], fill=c_arrow)
        if label:
            lx = xs + 10 * scale if label_side == "right" else xs - 10 * scale
            bbox = draw.textbbox((0, 0), label, font=f_arrow_lbl)
            lw = bbox[2] - bbox[0]
            if label_side == "left":
                lx -= lw
            mid_y = (y0s + y1s) // 2 - 7 * scale
            draw.text((lx, mid_y), label, font=f_arrow_lbl, fill=c_text_muted)

    def draw_horizontal_arrow(x0, x1, y, label=None):
        x0s = int(x0 * scale)
        x1s = int(x1 * scale)
        ys = int(y * scale)
        draw.line([(x0s, ys), (x1s, ys)], fill=c_arrow, width=max(1, int(1.5 * scale)))
        ah = 7 * scale
        aw = 5 * scale
        draw.polygon([(x1s, ys), (x1s - ah, ys - aw), (x1s - ah, ys + aw)], fill=c_arrow)
        if label:
            bbox = draw.textbbox((0, 0), label, font=f_arrow_lbl)
            lw = bbox[2] - bbox[0]
            draw.text(((x0s + x1s) // 2 - lw // 2, ys - 14 * scale), label, font=f_arrow_lbl, fill=c_text_muted)

    # Outer border container
    draw.rounded_rectangle([20 * scale, 16 * scale, 1030 * scale, 784 * scale], radius=10 * scale, outline=(203, 213, 225, 255), width=max(1, scale))

    # 1. Main Header Title
    title_text = "Every screen reaches MySQL only through a DAO and JDBC"
    t_bbox = draw.textbbox((0, 0), title_text, font=f_main_title)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((w - t_w) // 2, 32 * scale), title_text, font=f_main_title, fill=(15, 23, 42, 255))

    # 2. User Pills at the top
    draw_user_pill(210, 92, "Administrator")
    draw_user_pill(410, 92, "Dining Customer")

    # Down arrows from users to Presentation layer
    draw_down_arrow(210, 110, 144)
    draw_down_arrow(410, 110, 144)

    # Column coordinates
    left_x0, left_x1 = 55, 595
    right_x0, right_x1 = 665, 995

    # 3. Presentation Layer
    draw_card(
        (left_x0, 144, left_x1, 244),
        bg_color=(239, 246, 255, 255),       # Soft blue
        border_color=(37, 99, 235, 255),      # Blue 600
        title="Presentation layer: gui package (Java Swing)",
        subtitle_lines=[
            "MainFrame, AuthPanel, AdminDashboardPanel, CustomerDashboardPanel",
            "ReservationDialog, TablesDialog, SearchReservationDialog, ModifyDialog, CancelDialog",
            "Event handling via ActionListeners & TableSelection on Event Dispatch Thread"
        ],
        title_color=(29, 78, 216, 255)
    )

    # 4. Business Rules: util
    draw_card(
        (right_x0, 144, right_x1, 244),
        bg_color=(254, 252, 232, 255),       # Soft amber
        border_color=(217, 119, 6, 255),      # Amber 600
        title="Business rules: util package",
        subtitle_lines=[
            "ValidationUtil: Phone, email, date checks",
            "PasswordUtil: Salt generation & SHA-256",
            "UserSession: Logged-in session state",
            "DBConnection: Centralized connection factory"
        ],
        title_color=(180, 83, 9, 255)
    )

    # Arrow from Presentation to Business Rules
    draw_horizontal_arrow(left_x1, right_x0, 194, "rules / validation")

    # Down arrow from Presentation to DAO
    draw_down_arrow(325, 244, 308, "method calls / model objects", label_side="right")

    # 5. Data Access Layer: dao
    draw_card(
        (left_x0, 308, left_x1, 416),
        bg_color=(240, 253, 244, 255),       # Soft emerald
        border_color=(16, 185, 129, 255),     # Emerald 500
        title="Data access layer: dao package",
        subtitle_lines=[
            "ReservationDAO: Full booking CRUD, atomic multi-table transactions",
            "TableDAO: Dynamic slot availability with NOT EXISTS conflict check",
            "CustomerDAO: Customer record management with generated keys",
            "UserDAO: Authentication queries, customer registration, admin auto-seed"
        ],
        title_color=(4, 120, 87, 255)
    )

    # 6. Data Objects: model
    draw_card(
        (right_x0, 308, right_x1, 426),
        bg_color=(250, 245, 255, 255),       # Soft purple
        border_color=(147, 51, 234, 255),     # Purple 600
        title="Data objects: model package",
        subtitle_lines=[
            "RestaurantTable: tableId, number, capacity, status",
            "Customer: customerId, name, phone, email",
            "Reservation: reservationId, tableId, date, time",
            "ReservationDetail: Multi-table JOIN view",
            "User: userId, username, password_hash, salt, role"
        ],
        title_color=(109, 40, 217, 255)
    )

    # Arrow from DAO to Model
    draw_horizontal_arrow(left_x1, right_x0, 362, "creates / returns")

    # Down arrow from DAO to JDBC
    draw_down_arrow(325, 416, 478, "SQL statements / ResultSet rows", label_side="right")

    # 7. JDBC Layer
    draw_card(
        (left_x0, 478, left_x1, 584),
        bg_color=(248, 250, 252, 255),       # Slate 50
        border_color=(71, 85, 105, 255),      # Slate 600
        title="JDBC: MySQL Connector/J driver (mysql-connector-j-9.7.0.jar)",
        subtitle_lines=[
            "java.sql.Connection, PreparedStatement, Statement, ResultSet",
            "Transaction Control: setAutoCommit(false), commit(), rollback()",
            "Parameterized bindings: setString(), setInt(), setDate(), setTime()",
            "Automatic resource cleanup via try-with-resources"
        ],
        title_color=(30, 41, 59, 255)
    )

    # Down arrow from JDBC to Database
    draw_down_arrow(325, 584, 646, "jdbc:mysql://localhost:3306/restaurant_db", label_side="right")

    # 8. MySQL Database Container
    draw_card(
        (left_x0, 646, left_x1, 756),
        bg_color=(240, 249, 255, 255),       # Sky blue
        border_color=(2, 132, 199, 255),      # Sky 600
        title="MySQL Relational Database: restaurant_db",
        subtitle_lines=[
            "restaurant_tables: Physical dining tables & seating capacity (2 to 8 seats)",
            "customers: Dining customer profiles & contact phone numbers",
            "reservations: Relational bookings linking customers & tables with slot date/time",
            "users: Secure user accounts with unique usernames, SHA-256 hashes & salts"
        ],
        title_color=(3, 105, 161, 255)
    )

    # Resize back down using high-quality Lanczos resampling
    final_img = img.resize((1050, 800), Image.Resampling.LANCZOS)
    output_path = "layers_of_the_application.png"
    final_img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Saved high-resolution diagram: {output_path}")

if __name__ == "__main__":
    draw_diagram()
