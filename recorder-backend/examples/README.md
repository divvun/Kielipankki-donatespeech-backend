# MAUI Integration Examples

This directory contains example files for integrating the recorder backend with
a .NET MAUI application.

## Files

### `RecorderApiService.cs`

Example service wrapper showing how to:

- Configure the API client with platform-specific base URLs
- Call schedule and theme endpoints
- Upload recordings with metadata
- Delete recordings

**Usage in MAUI app:**

1. Generate the API client using NSwag or Kiota (see main README)
2. Copy this service to your MAUI project
3. Register in `MauiProgram.cs`:
   ```csharp
   builder.Services.AddSingleton<RecorderApiService>();
   ```
4. Inject and use in your pages/view models:
   ```csharp
   public class MainViewModel
   {
       private readonly RecorderApiService _api;
       
       public MainViewModel(RecorderApiService api)
       {
           _api = api;
       }
       
       public async Task LoadSchedules()
       {
           var schedules = await _api.GetSchedulesAsync();
           // Use schedules...
       }
   }
   ```

## Platform-Specific Configuration

The example shows how to handle different platforms:

- **macOS/iOS**: Use `http://localhost:8000`
- **Android Emulator**: Use `http://10.0.2.2:8000`
- **Android Physical**: Use your Mac's LAN IP (e.g.,
  `http://192.168.1.100:8000`)

## Next Steps

1. Start the backend: `cd .. && ./setup-local.sh`
2. Generate the C# client using `nswag.example.json` or Kiota
3. Copy and adapt `RecorderApiService.cs` to your MAUI project
4. Test on each platform (Mac, iOS simulator, Android emulator)
