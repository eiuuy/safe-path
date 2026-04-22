import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class SosButton extends StatelessWidget {
  final VoidCallback onPressed; // Обязательный параметр

  const SosButton({super.key, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onLongPress: onPressed,
      child: Container(
        width: 80,
        height: 80,
        decoration: BoxDecoration(
          color: Colors.redAccent,
          shape: BoxShape.circle,
          boxShadow: [
            BoxShadow(color: Colors.red.withOpacity(0.4), blurRadius: 20),
          ],
        ),
        child: const Center(
          child: Text(
            "SOS",
            style: TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}
