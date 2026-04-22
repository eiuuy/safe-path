import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SafeInfoCard extends StatelessWidget {
  final String status;
  const SafeInfoCard({super.key, required this.status});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(30),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.shield, color: AppColors.safetyGreen),
          const SizedBox(width: 10),
          Text(
            status,
            style: const TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 16,
              color: AppColors.primaryBlue,
            ),
          ),
        ],
      ),
    );
  }
}
