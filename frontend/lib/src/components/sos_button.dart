import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:permission_handler/permission_handler.dart';

class SosButton extends StatelessWidget {
  const SosButton({super.key});

  Future<void> _makeCall(BuildContext context) async {
    // 1. Спрашиваем разрешение
    var status = await Permission.phone.request();

    if (status.isGranted) {
      final Uri launchUri = Uri(scheme: 'tel', path: '102');
      if (await canLaunchUrl(launchUri)) {
        await launchUrl(launchUri);
      } else {
        if (context.mounted) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(const SnackBar(content: Text('Ошибка звонка')));
        }
      }
    } else {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Нет разрешения на звонок!')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton(
      backgroundColor: Colors.red,
      onPressed: () => _makeCall(context),
      child: const Text("SOS", style: TextStyle(fontWeight: FontWeight.bold)),
    );
  }
}
