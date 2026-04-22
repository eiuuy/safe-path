import 'package:flutter/material.dart';
import '../screens/teenager_dashboard.dart';
import '../screens/parent_dashboard.dart';
import '../screens/partner_dashboard.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HomeRouter extends StatelessWidget {
  const HomeRouter({super.key});

  Future<String?> _getRole() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('user_role');
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String?>(
      future: _getRole(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }

        final role = snapshot.data;
        if (role == 'teenager') return TeenagerDashboard();
        if (role == 'parent') return const ParentDashboard();
        return const PartnerDashboard();
      },
    );
  }
}
