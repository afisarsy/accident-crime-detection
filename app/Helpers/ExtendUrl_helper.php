<?php

use CodeIgniter\HTTP\URI;

if (! function_exists('backend_url'))
{
	/**
	 * Returns the backend URL as defined by the App config.
	 * Base URLs are trimmed site URLs without the index page.
	 *
	 * @param  mixed  $relativePath URI string or array of URI segments
	 * @param  string $scheme
	 * @return string
	 */
	function backend_url($relativePath = '', string $scheme = null): string
	{
		$config            = clone config('App');
		$config->indexPage = '';

		// If a full URI was passed then convert it
		if (is_int(strpos($relativePath, '://')))
			{
				$full         = new URI($relativePath);
				$relativePath = URI::createURIString(null, null, $full->getPath(), $full->getQuery(), $full->getFragment());
			}
		
		

		$relativePath = URI::removeDotSegments($relativePath);

		// Build the full URL based on $config and $relativePath
		$url = rtrim($config->backendURL, '/ ') . '/';

		$url .= $relativePath;

		$uri = new URI($url);

		// Check if the baseURL scheme needs to be coerced into its secure version
		if ($config->forceGlobalSecureRequests && $uri->getScheme() === 'http')
		{
			$uri->setScheme('https');
		}

		return $uri;
	}
}

?>