import 'package:flutter/material.dart';
import 'app_colors.dart'; // Импортируем цвета из соседнего файла

class AppTheme {
  static final ThemeData lightTheme = ThemeData(
    primaryColor: AppColors.primaryBlue,
    scaffoldBackgroundColor: AppColors.background,
    useMaterial3: true,
    colorScheme: const ColorScheme.light(
      primary: AppColors.primaryBlue,
      secondary: AppColors.safetyGreen,
      error: AppColors.alertRed,
    ),
    // Можно добавить настройки для кнопок, текста и т.д.
  );
}
