import 'package:flutter/material.dart';
import 'src/screens/map_screen.dart';
import 'src/screens/login_screen.dart';

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
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: const Color(0xFFF5F6FA),
      ),
      // Стартуем с логина, чтобы защитить приложение
      home: LoginScreen(),
    );
  }
}
