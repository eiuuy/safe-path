import 'package:flutter/material.dart';
import 'src/theme/app_theme.dart'; // Подключаем тему
import 'src/screens/login_screen.dart'; // Подключаем экран логина

void main() {
  runApp(const SafePathApp());
}

class SafePathApp extends StatelessWidget {
  const SafePathApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'E.C.H.O. Mate',
      // Теперь используем наш класс AppTheme
      theme: AppTheme.lightTheme,
      home: const LoginScreen(),
    );
  }
}
