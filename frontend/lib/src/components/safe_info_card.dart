import 'package:flutter/material.dart';
import '../theme/app_colors.dart'; // Предполагаю, что файл с цветами у тебя лежит тут

class SafeInfoCard extends StatelessWidget {
  final String status;
  final Color? statusColor; // Добавили параметр для цвета
  final VoidCallback? onTap; // Добавили действие при нажатии

  const SafeInfoCard({
    super.key,
    required this.status,
    this.statusColor, // Цвет необязателен (будет синим по умолчанию)
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    // Если цвет не передан, используем primaryBlue из твоего AppColors
    final color = statusColor ?? AppColors.primaryBlue;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
          border: Border.all(
            color: color.withAlpha(50),
          ), // Тонкая рамка цвета статуса
          boxShadow: [
            BoxShadow(
              color: color.withAlpha(20),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Row(
          children: [
            Icon(
              Icons.info_outline,
              color: color,
            ), // Иконка теперь тоже красится в цвет статуса
            const SizedBox(width: 10),
            Expanded(
              // Защита от длинного текста
              child: Text(
                status,
                style: TextStyle(fontWeight: FontWeight.bold, color: color),
                overflow:
                    TextOverflow.ellipsis, // Если текст длинный, добавит "..."
              ),
            ),
          ],
        ),
      ),
    );
  }
}
