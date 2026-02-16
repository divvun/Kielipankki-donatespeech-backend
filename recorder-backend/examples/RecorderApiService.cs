// Example service wrapper for MAUI app
// This shows how to use the generated RecorderApiClient in your MAUI application
// 
// Prerequisites:
// 1. Generate the client using NSwag or Kiota (see README.md)
// 2. Add this service to your MAUI dependency injection

using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

namespace KielipankkiRecorder.Services
{
    /// <summary>
    /// Service for interacting with the recorder backend API
    /// </summary>
    public class RecorderApiService
    {
        private readonly RecorderApiClient _apiClient;
        private readonly HttpClient _uploadHttpClient;

        public RecorderApiService()
        {
            // Configure API client with platform-specific base URL
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri(GetBaseUrl()),
                Timeout = TimeSpan.FromSeconds(30)
            };

            _apiClient = new RecorderApiClient(httpClient);
            _uploadHttpClient = new HttpClient(); // For direct blob uploads
        }

        /// <summary>
        /// Get platform-specific base URL for the backend
        /// </summary>
        private static string GetBaseUrl()
        {
            #if ANDROID
                // Android emulator uses 10.0.2.2 to access host's localhost
                // Physical devices need the Mac's LAN IP
                return DeviceInfo.DeviceType == DeviceType.Virtual 
                    ? "http://10.0.2.2:8000"
                    : "http://192.168.1.100:8000"; // Replace with your Mac's IP
            #elif IOS
                return "http://localhost:8000";
            #elif MACCATALYST
                return "http://localhost:8000";
            #else
                return "http://localhost:8000";
            #endif
        }

        /// <summary>
        /// Load all available schedules
        /// </summary>
        public async Task<List<ScheduleListItem>> GetSchedulesAsync()
        {
            return await _apiClient.Schedule.GetAsync();
        }

        /// <summary>
        /// Load a specific schedule by ID
        /// </summary>
        public async Task<Schedule> GetScheduleAsync(string scheduleId)
        {
            return await _apiClient.Schedule[scheduleId].GetAsync();
        }

        /// <summary>
        /// Load all available themes
        /// </summary>
        public async Task<List<ThemeListItem>> GetThemesAsync()
        {
            return await _apiClient.Theme.GetAsync();
        }

        /// <summary>
        /// Load a specific theme by ID
        /// </summary>
        public async Task<Theme> GetThemeAsync(string themeId)
        {
            return await _apiClient.Theme[themeId].GetAsync();
        }

        /// <summary>
        /// Upload an audio recording
        /// </summary>
        /// <param name="audioFilePath">Path to the audio file</param>
        /// <param name="clientId">Unique client identifier (UUID v4)</param>
        /// <param name="sessionId">Optional session identifier (UUID v4)</param>
        /// <param name="metadata">Additional metadata</param>
        public async Task<bool> UploadRecordingAsync(
            string audioFilePath,
            Guid clientId,
            Guid? sessionId = null,
            RecordingMetadata metadata = null)
        {
            try
            {
                // Step 1: Initialize upload and get presigned URL
                var uploadRequest = new InitUploadRequest
                {
                    Filename = Path.GetFileName(audioFilePath),
                    Metadata = new UploadMetadata
                    {
                        ClientId = clientId.ToString(),
                        SessionId = sessionId?.ToString(),
                        ContentType = GetContentType(audioFilePath),
                        Timestamp = DateTime.UtcNow.ToString("o"),
                        Duration = metadata?.Duration,
                        Language = metadata?.Language ?? "fi"
                    }
                };

                var initResponse = await _apiClient.Upload.PostAsync(uploadRequest);

                // Step 2: Upload file directly to blob storage using presigned URL
                using var fileStream = File.OpenRead(audioFilePath);
                using var streamContent = new StreamContent(fileStream);
                streamContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue(
                    uploadRequest.Metadata.ContentType);

                var uploadResponse = await _uploadHttpClient.PutAsync(
                    initResponse.PresignedUrl, 
                    streamContent);

                return uploadResponse.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                // Log error
                Console.WriteLine($"Upload failed: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Delete all recordings for a client
        /// </summary>
        public async Task<bool> DeleteClientRecordingsAsync(Guid clientId)
        {
            try
            {
                await _apiClient.Recordings[clientId.ToString()].DeleteAsync();
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Delete all recordings for a session
        /// </summary>
        public async Task<bool> DeleteSessionRecordingsAsync(Guid clientId, Guid sessionId)
        {
            try
            {
                await _apiClient.Recordings[clientId.ToString()][sessionId.ToString()].DeleteAsync();
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Delete a specific recording
        /// </summary>
        public async Task<bool> DeleteRecordingAsync(Guid clientId, Guid sessionId, Guid recordingId)
        {
            try
            {
                await _apiClient.Recordings[clientId.ToString()][sessionId.ToString()][recordingId.ToString()].DeleteAsync();
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Get content type based on file extension
        /// </summary>
        private static string GetContentType(string filePath)
        {
            var extension = Path.GetExtension(filePath).ToLowerInvariant();
            return extension switch
            {
                ".m4a" => "audio/m4a",
                ".flac" => "audio/flac",
                ".wav" => "audio/wav",
                ".opus" => "audio/opus",
                ".amr" => "audio/amr",
                ".caf" => "audio/x-caf",
                _ => "application/octet-stream"
            };
        }
    }

    /// <summary>
    /// Additional recording metadata
    /// </summary>
    public class RecordingMetadata
    {
        public double? Duration { get; set; }
        public string Language { get; set; }
    }

    // Register in MauiProgram.cs:
    // builder.Services.AddSingleton<RecorderApiService>();
}
