plugins {
    id("com.android.application")
}

android {
    namespace = "com.pin.pin2twf"
    compileSdk = 37

    defaultConfig {
        applicationId = "com.pin.pin2twf.watchface"
        minSdk = 34 // Wear OS 5+, required for Watch Face Format v2
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            // R8 strips the generated R classes so the APK ships without classes.dex.
            isMinifyEnabled = true
            // Never shrink resources: nothing references watchface.xml from code.
            isShrinkResources = false
            // Signed with the local debug key so the release APK can be sideloaded as-is.
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}
