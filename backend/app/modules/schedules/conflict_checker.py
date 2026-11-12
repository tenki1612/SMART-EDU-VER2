"""
KI-01: Thuật toán phát hiện xung đột thời khóa biểu thời gian thực.

Hai khoảng thời gian [A_start, A_end] và [B_start, B_end] giao nhau
khi và chỉ khi: (A_start < B_end) AND (A_end > B_start).

Edge cases (KI-01):
  1. Buổi học liền kề không xung đột (ca 1 kết thúc 18:00, ca 2 bắt đầu 18:00).
  2. Bỏ qua các buổi đã hủy (status == 'CANCELLED') và đã soft-delete.
  3. Loại trừ chính buổi đang sửa (exclude_session_id).
"""


def is_time_overlap(start_a: str, end_a: str, start_b: str, end_b: str) -> bool:
    """Kiểm tra 2 khoảng giờ (định dạng "HH:MM") có chồng lấn hay không."""
    return (start_a < end_b) and (end_a > start_b)


def is_valid_time_range(start_time: str, end_time: str) -> bool:
    """Khung giờ hợp lệ khi giờ kết thúc lớn hơn giờ bắt đầu."""
    return start_time < end_time


def describe_conflict(
    conflict_type: str,
    classroom_code: str = "",
    teacher_name: str = "",
    class_code: str = "",
    start_time: str = "",
    end_time: str = "",
) -> str:
    """Sinh thông điệp tiếng Việt mô tả chi tiết xung đột."""
    if conflict_type == "CLASSROOM":
        return (
            f"Phòng học {classroom_code} đã có lớp {class_code} học trong khung giờ "
            f"{start_time} - {end_time}. Vui lòng chọn phòng khác hoặc đổi khung giờ."
        )
    return (
        f"Giáo viên {teacher_name} đang dạy lớp {class_code} trong khung giờ "
        f"{start_time} - {end_time}. Vui lòng chọn giáo viên khác hoặc đổi khung giờ."
    )
