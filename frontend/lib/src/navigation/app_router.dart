import 'package:flutter/material.dart';
import '../screens/map_screen.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    return MaterialPageRoute(builder: (_) => MapScreen());
  }
}
